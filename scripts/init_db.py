import asyncio

from unisphere.models import close_db, init_db


async def main():
    await init_db()
    await close_db()


if __name__ == "__main__":
    asyncio.run(main())
