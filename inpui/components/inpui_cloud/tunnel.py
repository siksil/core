"""Cloudflare Tunnel process manager for Inpui Cloud."""

import asyncio
import logging
from typing import Optional

_LOGGER = logging.getLogger(__name__)

# Default binary path; assume cloudflared is installed natively in the base image
CLOUDFLARED_BIN = "cloudflared"


class CloudflareTunnel:
    """Manager for the cloudflared tunnel process."""

    def __init__(self, token: str, binary: str = CLOUDFLARED_BIN):
        self.token = token
        self.binary = binary
        self.proc: Optional[asyncio.subprocess.Process] = None
        self._should_run = False

    async def start_managed(self):
        """Entry point for entry.async_create_background_task.

        Runs the tunnel loop and handles CancelledError gracefully
        so HA can cancel this task on unload.
        """
        self._should_run = True
        try:
            await self._run_loop()
        except asyncio.CancelledError:
            _LOGGER.info("Tunnel task cancelled, shutting down cloudflared...")
            await self._terminate_proc()

    async def start(self):
        """Legacy start — spawns the run loop as a free task."""
        self._should_run = True
        asyncio.create_task(self._run_loop())

    async def stop(self):
        """Stop the cloudflared process."""
        self._should_run = False
        await self._terminate_proc()

    async def _terminate_proc(self):
        """Terminate the subprocess if running."""
        if self.proc and self.proc.returncode is None:
            try:
                self.proc.terminate()
                await asyncio.wait_for(self.proc.wait(), timeout=5)
            except asyncio.TimeoutError:
                _LOGGER.warning("cloudflared did not terminate, killing...")
                self.proc.kill()
            except Exception as err:
                _LOGGER.error("Error stopping cloudflared: %s", err)

    async def _run_loop(self):
        """Keep the tunnel running with exponential backoff."""
        backoff = 1
        while self._should_run:
            _LOGGER.info("Starting cloudflared tunnel...")
            try:
                self.proc = await asyncio.create_subprocess_exec(
                    self.binary,
                    "tunnel",
                    "--no-autoupdate",
                    "run",
                    "--token",
                    self.token,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                return_code = await self.proc.wait()
                if return_code != 0:
                    _LOGGER.error("cloudflared exited with code %s", return_code)

            except FileNotFoundError:
                _LOGGER.error(
                    "cloudflared binary not found at %s. "
                    "See INSTRUCTIONS.txt Part 2 Step 2.",
                    self.binary,
                )
            except asyncio.CancelledError:
                raise  # Re-raise so start_managed handles cleanup
            except Exception as err:
                _LOGGER.error("Failed to start cloudflared: %s", err)

            if not self._should_run:
                break

            _LOGGER.info("Retrying cloudflared in %s seconds...", backoff)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 60)
