
import asyncio
from workflows.seo_workflow import run_seo_workflow


async def main():
    print("=" * 60)
    print("AUTOGEN MULTI-AGENT SEO CONTENT GENERATOR")
    print("=" * 60)

    result = await run_seo_workflow(
        topic="Best AI Tools for Small Businesses in 2026",
        audience="Small Business Owners",
        word_count=800,
    )

    print("\n" + "=" * 60)
    print("RESEARCH AGENT OUTPUT")
    print("=" * 60)
    print(result["research"])

    print("\n" + "=" * 60)
    print("CONTENT WRITER OUTPUT")
    print("=" * 60)
    print(result["article"])

    print("\n" + "=" * 60)
    print("SEO OPTIMIZATION OUTPUT")
    print("=" * 60)
    print(result["optimized_article"])

    print("\n" + "=" * 60)
    print("CONTENT REVIEWER OUTPUT")
    print("=" * 60)
    print(result["review"])

    print("\n" + "=" * 60)
    print("WORKFLOW COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
