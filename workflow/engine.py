class Step:
    def __init__(self, name, handler):
        self.name = name
        self.handler = handler

    def run(self, context):
        result = self.handler(context)
        return result or context


class Workflow:
    def __init__(self, name):
        self.name = name
        self.steps = []

    def add_step(self, name, handler):
        self.steps.append(Step(name, handler))
        return self

    def run(self, context=None):
        context = context or {}
        log = []
        for step in self.steps:
            try:
                context = step.run(context)
                log.append({"step": step.name, "status": "success", "context": dict(context)})
            except Exception as e:
                log.append({"step": step.name, "status": "error", "error": str(e)})
                break
        return log


class WorkflowRegistry:
    _workflows = {}

    @classmethod
    def register(cls, workflow):
        cls._workflows[workflow.name] = workflow

    @classmethod
    def get(cls, name):
        return cls._workflows.get(name)

    @classmethod
    def all(cls):
        return list(cls._workflows.keys())


# --- Register built-in workflows ---

def _start(ctx):
    ctx["status"] = "started"
    return ctx

def _validate(ctx):
    if not ctx.get("input"):
        raise ValueError("Missing input data")
    ctx["validated"] = True
    return ctx

def _process(ctx):
    ctx["result"] = f"Processed: {ctx.get('input', '')}"
    return ctx

def _notify(ctx):
    ctx["notified"] = True
    return ctx


data_pipeline = Workflow("Data Pipeline")
data_pipeline.add_step("Start", _start)
data_pipeline.add_step("Validate Input", _validate)
data_pipeline.add_step("Process Data", _process)
data_pipeline.add_step("Notify", _notify)
WorkflowRegistry.register(data_pipeline)


def _init(ctx):
    ctx["status"] = "initialized"
    return ctx

def _approve(ctx):
    ctx["approved"] = True
    return ctx

def _deploy(ctx):
    ctx["deployed"] = True
    ctx["result"] = "Deployment successful"
    return ctx


deploy_workflow = Workflow("Deployment Workflow")
deploy_workflow.add_step("Initialize", _init)
deploy_workflow.add_step("Approval Check", _approve)
deploy_workflow.add_step("Deploy", _deploy)
WorkflowRegistry.register(deploy_workflow)


def _collect(ctx):
    ctx["data_collected"] = True
    return ctx

def _analyze(ctx):
    ctx["analysis"] = f"Score: {len(ctx.get('input', '')) * 7}"
    return ctx

def _report(ctx):
    ctx["report"] = "Report generated"
    return ctx


report_workflow = Workflow("Report Generator")
report_workflow.add_step("Collect Data", _collect)
report_workflow.add_step("Analyze", _analyze)
report_workflow.add_step("Generate Report", _report)
WorkflowRegistry.register(report_workflow)
