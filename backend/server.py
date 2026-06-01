"""
Development server entry point
"""

import uvicorn

from api.app import create_app


def main() -> None:
    uvicorn.run(
        create_app(),
        host="127.0.0.1",
        port=5000,
        access_log=False,
    )


if __name__ == "__main__":
    main()
