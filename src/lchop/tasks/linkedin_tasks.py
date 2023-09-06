import asyncio
import functools

from lchop.task_context import TaskContext
from lchop.work_context import WorkContext
from loguru import logger

def with_delay(delay_seconds=1):  # Set default delay to 1 second
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            await asyncio.sleep(delay_seconds)
            return await func(*args, **kwargs)
        return wrapper
    return decorator


@TaskContext.register_task
async def hello_world_template(task, dsl_ctx: WorkContext):
    try:
        # Extracting the TemplateContext
        template_ctx = dsl_ctx.template_ctx

        # Define the template string
        template_str = "Hello {{ world_var }}!"

        # Set a global variable in the template context
        template_ctx.set_variable("world_var", "World")

        # Render the template
        rendered_str = template_ctx.render_template(template_str)

        logger.info(f"Successfully rendered the hello world command: {rendered_str}")

        return rendered_str

    except Exception as e:
        logger.error(f"Failed to execute the hello world command: {str(e)}")
        raise


@with_delay()
@TaskContext.register_task
async def navigate_to_url(task, dsl_ctx: WorkContext):
    try:
        url = task.get("url", "")
        page = dsl_ctx.browser_ctx.page
        await page.goto(url)
        logger.info(f"Navigated to URL: {url}")
    except Exception as e:
        logger.error(f"Failed to navigate to URL: {str(e)}")
        raise

@with_delay()
@TaskContext.register_task
async def click_element(task, dsl_ctx: WorkContext):
    try:
        browser_ctx = dsl_ctx.browser_ctx
        selector = task.get("selector", "")
        page = await browser_ctx.newPage()
        await page.click(selector)
        logger.info(f"Clicked element: {selector}")
    except Exception as e:
        logger.error(f"Failed to click element: {str(e)}")
        raise

@with_delay()
@TaskContext.register_task
async def fill_linkedin(task, dsl_ctx: WorkContext):
    try:
        browser_ctx = dsl_ctx.browser_ctx
        selector = task.get("selector", "")
        value = task.get("value", "")
        page = await browser_ctx.newPage()
        await page.type(selector, value)
        logger.info(f"Filled form field {selector} with value {value}")
    except Exception as e:
        logger.error(f"Failed to fill form: {str(e)}")
        raise



class LinkedInGroup:
    name: str

class LinkedInProfile:
    groups: list
    lastName: str
    memorialized: bool
    objectUrn: str
    geoRegion: str
    saved: bool
    openLink: bool
    premium: bool
    currentPositions: list
    entityUrn: str
    viewed: bool
    spotlightBadges: list
    trackingId: str
    blockThirdPartyDataSharing: bool
    summary: str
    pendingInvitation: bool
    pastPositions: list
    degree: int
    fullName: str
    listCount: int
    firstName: str
    profilePictureDisplayImage: dict
    profileLink: str

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


@TaskContext.register_task
async def generate_profiles_page(task, dsl_ctx):
        data = task.profiles

        profiles = []

        for profile in data.elements:
            del profile['$recipeType']
            del profile['$anti_abuse_metadata']

            # create profile link
            urn = profile['entityUrn'].split(":")[3]
            urn = urn.replace("(", "")
            urn = urn.replace(")", "")
            profile['profileLink'] = f"https://www.linkedin.com/sales/lead/{urn}"

            pro = LinkedInProfile(**profile)
            profiles.append(pro)

        print(profiles[0].profilePictureDisplayImage)
        pro = profiles[0]
        full_img = pro.profilePictureDisplayImage['rootUrl'] + pro.profilePictureDisplayImage['artifacts'][0][
            'fileIdentifyingUrlPathSegment']
        print(full_img)
