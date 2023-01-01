from core.auth.models import RlcUser
from core.questionnaires.models import Questionnaire
from core.questionnaires.use_cases.finders import questionnaire_template_from_id
from core.records.use_cases.finders import record_from_id
from core.seedwork.use_case_layer import find, use_case
from core.static import PERMISSION_RECORDS_ADD_RECORD


@use_case(permissions=[PERMISSION_RECORDS_ADD_RECORD])
def publish_a_questionnaire(
    __actor: RlcUser,
    record=find(record_from_id),
    template=find(questionnaire_template_from_id),
):
    questionnaire = Questionnaire(record=record, template=template)
    questionnaire.save()
    return questionnaire


@use_case
def optimize_questionnaires(__actor: RlcUser):
    qs_1 = Questionnaire.objects.filter(template__rlc_id=__actor.org_id)
    qs_2: list[Questionnaire] = list(qs_1)
    for q in qs_2:
        q.put_in_folder(__actor)
