import yaml

from lchop.context.browser_context import BrowserContext
from lchop.context.task_context import TaskContext
from lchop.context.template_context import TemplateContext
from lchop.context.work_context import WorkContext


def generate_task_code_from_workflow(workflow_path, output_file_path, work_ctx):
    try:
        with open(workflow_path, "r") as stream:
            workflow_config = yaml.safe_load(stream)

        rendered = work_ctx.template_ctx.render_file_template(
            " task_function_template.j2", workflow=workflow_config.get("workflow")
        )

        with open(output_file_path, "w") as f:
            f.write(rendered)

        return {
            "success": True,
            "results": f"Successfully generated code in {output_file_path}",
        }

    except Exception as e:
        return {"success": False, "results": f"Failed to generate code: {str(e)}"}


# Example usage
if __name__ == "__main__":
    work_ctx = WorkContext(TaskContext(), TemplateContext(), BrowserContext())
    result = generate_task_code_from_workflow(
        "your_workflow.yaml", "generated_tasks.py", work_ctx
    )
    print(result)
