from apps.recordmanagement.serializers.questionnaire import QuestionnaireSerializer, RecordQuestionnaireSerializer, \
    RecordQuestionnaireDetailSerializer, CodeSerializer, \
    QuestionnaireFieldSerializer, QuestionnaireAnswerCreateFileSerializer, QuestionnaireAnswerCreateTextSerializer, \
    QuestionnaireFileSerializer
from apps.recordmanagement.models import Questionnaire, RecordQuestionnaire
from rest_framework.exceptions import ParseError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.none()
    serializer_class = QuestionnaireSerializer

    def get_queryset(self):
        return Questionnaire.objects.filter(rlc=self.request.user.rlc)

    def perform_create(self, serializer):
        return serializer.save()

    @action(detail=True, methods=['get'])
    def fields(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.fields.all()
        serializer = QuestionnaireFieldSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def files(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.files.all()
        serializer = QuestionnaireFileSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], permission_classes=[])
    def code(self, request, *args, **kwargs):
        serializer = CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if RecordQuestionnaire.objects.filter(code=serializer.validated_data['code']).exists():
            return Response({'code': serializer.validated_data['code']}, status=status.HTTP_200_OK)
        return Response({'non_field_errors': 'There is no questionnaire with this code.'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def publish(self, request, *args, **kwargs):
        serializer = RecordQuestionnaireSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(RecordQuestionnaireDetailSerializer(instance).data, status=status.HTTP_201_CREATED,
                        headers=headers)


class RecordQuestionnaireViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                                 mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = RecordQuestionnaire.objects.none()
    serializer_class = RecordQuestionnaireSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'partial_update']:
            return []
        return super().get_permissions()

    def get_queryset(self):
        if self.action in ['retrieve', 'partial_update']:
            return RecordQuestionnaire.objects.all()
        return RecordQuestionnaire.objects.filter(questionnaire__rlc=self.request.user.rlc)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'partial_update']:
            return RecordQuestionnaireDetailSerializer
        return super().get_serializer_class()

    def retrieve(self, request, *args, **kwargs):
        self.lookup_url_kwarg = 'pk'
        self.lookup_field = 'code'
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # save the fields
        for field in list(instance.questionnaire.fields.all()):
            if field.name in request.data and request.data[field.name]:
                data = {'record_questionnaire': instance.pk, 'field': field.pk, 'data': request.data[field.name]}
                if field.type == 'FILE':
                    answer_serializer = QuestionnaireAnswerCreateFileSerializer(data=data)
                else:
                    answer_serializer = QuestionnaireAnswerCreateTextSerializer(data=data)
                if answer_serializer.is_valid(raise_exception=False):
                    answer = answer_serializer.get_instance()
                    answer.encrypt()
                    answer.save()
                else:
                    raise ParseError({field.name: answer_serializer.errors['data']})
        # return
        serializer = self.get_serializer(instance)
        return Response(serializer.data)