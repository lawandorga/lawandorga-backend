from core.auth.models import RlcUser
from core.questionnaires.use_cases.questionnaire import (
    optimize_questionnaires,
    publish_a_questionnaire,
)
from core.seedwork.api_layer import Router

from . import schemas

router = Router()


@router.post(
    url="publish/",
    input_schema=schemas.InputPublishQuestionnaire,
    output_schema=schemas.OutputQuestionnaire,
)
def publish_questionnaire(data: schemas.InputPublishQuestionnaire, rlc_user: RlcUser):
    questionnaire = publish_a_questionnaire(
        rlc_user, folder=data.folder, template=data.template
    )
    return questionnaire


@router.post(
    url="optimize/",
)
def command__optimize(rlc_user: RlcUser):
    optimize_questionnaires(rlc_user)