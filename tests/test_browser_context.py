import asyncio
import pytest

from lchop.browser_context import BrowserContext


@pytest.fixture
def browser_context():
    context = BrowserContext(use_existing_browser=True, enable_request_interception=True)
    asyncio.get_event_loop().run_until_complete(context.launch_browser())
    yield context
    asyncio.get_event_loop().run_until_complete(context.close_browser())

@pytest.mark.asyncio
async def test_browser_launch(browser_context):
    assert browser_context.browser is not None
    assert browser_context.page is not None

@pytest.mark.asyncio
async def test_request_interception(browser_context):
    intercepted_requests = []

    async def intercept_request(intercepted_request):
        intercepted_requests.append(intercepted_request)
        await intercepted_request.continue_()

    browser_context.page.on('request', intercept_request)

    # Open a URL that triggers requests
    await browser_context.page.goto('https://www.example.com')

    assert len(intercepted_requests) > 0

@pytest.mark.asyncio
async def test_no_request_interception(browser_context):
    intercepted_requests = []

    async def intercept_request(intercepted_request):
        intercepted_requests.append(intercepted_request)
        await intercepted_request.continue_()

    browser_context.page.on('request', intercept_request)

    # Open a URL that triggers requests
    await browser_context.page.goto('https://www.example.com')

    assert len(intercepted_requests) == 0
