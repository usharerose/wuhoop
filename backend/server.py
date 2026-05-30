"""
Development server entry point
"""

import asyncio

from hypercorn.asyncio import serve
from hypercorn.config import Config

from .api.app import create_app


async def main() -> None:
    app = create_app()
    config = Config()
    config.bind = ["127.0.0.1:5000"]
    config.accesslog = "-"
    await serve(app, config)


if __name__ == "__main__":
    asyncio.run(main())
