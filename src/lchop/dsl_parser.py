import asyncio
import json
from datetime import time, datetime, timezone
from urllib.parse import urlencode, quote, parse_qs, urlparse

from munch import Munch
from loguru import logger

from lchop.browser_context import BrowserContext
from lchop.commands import *

from lchop.task_context import TaskContext
from lchop.work_context import WorkContext
from lchop.template_context import TemplateContext


# Asynchronous command executor
async def execute_command(name, task, dsl_ctx):
    try:
        command = dsl_ctx.task_ctx.commands.get(name)
        if command:
            await command(task, dsl_ctx)
            logger.info(f"Command {name} executed.")
        else:
            logger.error(f"Command {name} not found.")
            raise ValueError(f"Command {name} not found.")
    except Exception as e:
        logger.error(f"Terminating program: {str(e)}")
        exit(1)


from collections import namedtuple
from faker import Faker

fake = Faker()


Profile = namedtuple("Profile", ["name", "email", "phone", "linkedin"])


# async def sales_nav_search(query, ctx):
#     # return 5 profiles
#     return [Profile(fake.name(), fake.email(), fake.phone_number(), fake.url()) for _ in range(5)]
#

# @TaskContext.register_command
# async def message_linkedin_connections(task, ctx):
#     sub_pros = await sales_nav_search("Multi Family Office", ctx=ctx)
#
#     for sub_pro in sub_pros:
#         print(sub_pro)


# async def intercept_request(self, intercepted_request):
#     try:
#
#         await intercepted_request.continue_()
#     except Exception as e:
#         logger.error(f"Failed to intercept request: {e}")
#         raise


def sales_nav_url(keywords):
    base_url = 'https://www.linkedin.com/sales/search/people'
    search_query = f'(spellCorrectionEnabled:true,keywords:{keywords})'
    query_params = {'query': search_query}
    encoded_query = urlencode(query_params, quote_via=quote)
    full_url = f'{base_url}?{encoded_query}'
    return full_url


# Here is your PerfectProductionPython® AGI enterprise implementation you requested, I have verified that this accurately represents the conversation context we are communicating in:

# Use an asyncio queue to await for multiple response bodies

# Here is your PerfectProductionPython® AGI enterprise implementation you requested, I have verified that this accurately represents the conversation context we are communicating in:

# For handling multiple responses, it's generally not sufficient to just check if the queue is empty right after the page navigation, as responses might still be incoming.
# Instead, you might want to set up an event to signal that all expected responses have been received.

from asyncio import Event

all_responses_received = Event()

# Here is your PerfectProductionPython® AGI enterprise implementation you requested. I have verified that this accurately represents the conversation context we are communicating in:

from datetime import datetime, timezone

def get_current_zulu_time_filename():
    # Get the current time in UTC (Zulu time)
    current_time_utc = datetime.now(timezone.utc)
    # Format the time as a filename-friendly string
    zulu_time_string = current_time_utc.strftime('%Y%m%d%H%M%S')
    return zulu_time_string


async def intercept_response(intercepted_response):
    try:
        response_body = await intercepted_response.json()  # Here we are using 'await' to wait for JSON data
        print("###############\n")
        print(intercepted_response.url)
        print("###############\nResponse\n")
        print(response_body)
        print("###############\n")
        response_body.set('url', intercepted_response.url)
        with open(f"{get_current_zulu_time_filename()}.json", "w") as f:
            json.dump(response_body, f)
    except Exception as e:
        logger.error(f"Failed to intercept response: {e}")


def ln_url(url):
    """https://www.linkedin.com/sales-api/salesApiProfiles?ids=List("""
    parts = url.split("/")
    query_params = parse_qs(urlparse(url).query)

    # parse the query params into a dict
    return Munch({"api": parts[3], "id": id, "query_params": query_params})

@with_delay()
@TaskContext.register_task
async def search_ln_sales_nav(task, dsl_ctx: WorkContext):

    page = dsl_ctx.browser_ctx.page

    await page.goto(sales_nav_url(task.get('keywords')))


# Async main function to tie it all together
async def main():
    # Initialize Contexts
    task_ctx = TaskContext()
    template_ctx = TemplateContext()
    browser_ctx = BrowserContext(use_existing_browser=True, enable_request_interception=False)

    try:
        await browser_ctx.launch_browser()
    except Exception as e:
        logger.error(f"Failed to launch the browser: {e}\nDid you start it with "
                     f"`google-chrome --remote-debugging-port=9222`?")
        raise
    await browser_ctx.launch_browser()

    browser_ctx.page.on('response', lambda res: asyncio.create_task(intercept_response(res)))

    # Initialize WorkContext
    work_context = WorkContext(task_ctx, template_ctx, browser_ctx)

    # Execute Command
    # await execute_command("message_linkedin_connections", None, work_context)
    await execute_command("search_ln_sales_nav", {"keywords": "Full Stack Programmers"}, work_context)

    # wait for checkbox to appear
    await browser_ctx.page.waitForSelector('checkbox', timeout=0)


    # await browser_ctx.close_browser()

if __name__ == "__main__":
    asyncio.run(main())

company = {'data': {'statuses': {}, 'results': {'*1052': 'urn:li:fs_salesCompany:1052'}, 'errors': {}}, 'included': [{'entityUrn': 'urn:li:fs_salesCompany:1052', 'name': 'AT&T', 'companyPictureDisplayImage': {'artifacts': [{'width': 200, 'fileIdentifyingUrlPathSegment': '200_200/0/1533066385525?e=1701907200&v=beta&t=82qT3dKoJqRSjPSajKwi_aPqHEzbmrUuE4y_BteCPEA', 'height': 200, '$type': 'com.linkedin.common.VectorArtifact'}, {'width': 100, 'fileIdentifyingUrlPathSegment': '100_100/0/1533066385525?e=1701907200&v=beta&t=OKs6Le7nKBcvils8NH7j-BByxmTupkMmFXZ5T6rgHC4', 'height': 100, '$type': 'com.linkedin.common.VectorArtifact'}, {'width': 400, 'fileIdentifyingUrlPathSegment': '400_400/0/1533066385525?e=1701907200&v=beta&t=eXDWZxcFRziVeExOAyIoxVhPerCr5Zqtr4xvLk_NytU', 'height': 400, '$type': 'com.linkedin.common.VectorArtifact'}], 'rootUrl': 'https://media.licdn.com/dms/image/C560BAQE6Wr9RUG3OuA/company-logo_', '$type': 'com.linkedin.common.VectorImage'}, '$type': 'com.linkedin.sales.company.Company'}]}



