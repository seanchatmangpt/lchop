from loguru import logger

from lchop.tasks import TaskContext


@TaskContext.register_task
async def print_hello(work_ctx, message="Hello, World!"):
    logger.info(f"Executing task: print_hello")
    logger.info(f"Message: {message}")
    return {'success': True, 'results': f"Successfully printed: {message}"}

@TaskContext.register_task
async def print_goodbye(work_ctx, message="Goodbye, World!"):
    logger.info(f"Executing task: print_goodbye")
    logger.info(f"Message: {message}")
    return {'success': True, 'results': f"Successfully printed: {message}"}

