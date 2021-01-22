import base64
import json

from django.core.files.base import ContentFile
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from BookBSE.api.serializer import FacultySerializer
from .serializer import *

from ..models import *


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_professors(request):
    faculty_id = request.query_params.get('faculty_id', None)
    search = request.query_params.get('search', None)

    if faculty_id is not None:
        try:
            Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return Response(f"Faculty with faculty_id {faculty_id} NOT FOUND!")

    if faculty_id is not None:
        if search is None:
            professors_to_show = Professor.objects.filter(faculty__id=faculty_id)
        else:
            professors_to_show = Professor.objects.filter(Q(faculty__id=faculty_id),
                                                          Q(first_name__icontains=search) |
                                                          Q(last_name__icontains=search) |
                                                          Q(academic_rank__icontains=search) |
                                                          Q(research_axes__subject__icontains=search)
                                                          )
        serializer = ProfessorSerializer(professors_to_show, many=True)

        data = json.loads(json.dumps(serializer.data))

        for x in data:
            if x['academic_rank'] == 'Assistant Professor':
                x['academic_rank'] = 'استادیار'
            elif x['academic_rank'] == 'Associate Professor':
                x['academic_rank'] = 'دانشیار'
            elif x['academic_rank'] == 'Professor':
                x['academic_rank'] = 'استاد'

            free_times_list = []
            for free_time_id in x['free_times']:
                free_time = Time.objects.get(time_id=free_time_id)

                serializer = TimeSerializer(free_time)
                time_data = json.loads(json.dumps(serializer.data))

                if time_data['weekday'] == 'Saturday':
                    time_data['weekday'] = 'شنبه'
                elif time_data['weekday'] == 'Sunday':
                    time_data['weekday'] = 'یکشنبه'
                elif time_data['weekday'] == 'Monday':
                    time_data['weekday'] = 'دوشنبه'
                elif time_data['weekday'] == 'Tuesday':
                    time_data['weekday'] = 'سه‌شنبه'
                elif time_data['weekday'] == 'Wednesday':
                    time_data['weekday'] = 'چهارشنبه'
                elif time_data['weekday'] == 'Thursday':
                    time_data['weekday'] = 'پنج‌شنبه'
                elif time_data['weekday'] == 'Friday':
                    time_data['weekday'] = 'جمعه'

                time = time_data['weekday'] + ' ' + ':'.join(time_data['start_time'].split(':')[:2]) + "-" + \
                       ':'.join(time_data['end_time'].split(':')[:2])

                free_times_list.append(time)

            x['free_times'] = free_times_list

            research_axes_list = []
            for research_axis_id in x['research_axes']:
                research_axis = ResearchAxis.objects.get(research_axis_id=research_axis_id)

                serializer = ResearchAxisSerializer(research_axis)
                data_research_axis = json.loads(json.dumps(serializer.data))

                research_axes_list.append(data_research_axis['subject'])

            x['research_axes'] = research_axes_list
        return Response(data, status=status.HTTP_200_OK)
    else:
        if search is None:
            professors_to_show = Professor.objects.all()
        else:
            professors_to_show = Professor.objects.filter(Q(first_name__icontains=search) |
                                                          Q(last_name__icontains=search) |
                                                          Q(faculty__name__icontains=search) |
                                                          Q(academic_rank__icontains=search) |
                                                          Q(research_axes__subject__icontains=search)
                                                          )
        serializer = ProfessorSerializer(professors_to_show, many=True)

        data = json.loads(json.dumps(serializer.data))

        for x in data:
            if x['academic_rank'] == 'Assistant Professor':
                x['academic_rank'] = 'استادیار'
            elif x['academic_rank'] == 'Associate Professor':
                x['academic_rank'] = 'دانشیار'
            elif x['academic_rank'] == 'Professor':
                x['academic_rank'] = 'استاد'

            free_times_list = []
            for free_time_id in x['free_times']:
                free_time = Time.objects.get(time_id=free_time_id)

                serializer = TimeSerializer(free_time)
                time_data = json.loads(json.dumps(serializer.data))

                if time_data['weekday'] == 'Saturday':
                    time_data['weekday'] = 'شنبه'
                elif time_data['weekday'] == 'Sunday':
                    time_data['weekday'] = 'یکشنبه'
                elif time_data['weekday'] == 'Monday':
                    time_data['weekday'] = 'دوشنبه'
                elif time_data['weekday'] == 'Tuesday':
                    time_data['weekday'] = 'سه‌شنبه'
                elif time_data['weekday'] == 'Wednesday':
                    time_data['weekday'] = 'چهارشنبه'
                elif time_data['weekday'] == 'Thursday':
                    time_data['weekday'] = 'پنج‌شنبه'
                elif time_data['weekday'] == 'Friday':
                    time_data['weekday'] = 'جمعه'

                time = time_data['weekday'] + ' ' + ':'.join(time_data['start_time'].split(':')[:2]) + "-" + \
                       ':'.join(time_data['end_time'].split(':')[:2])

                free_times_list.append(time)

            x['free_times'] = free_times_list

            research_axes_list = []
            for research_axis_id in x['research_axes']:
                research_axis = ResearchAxis.objects.get(research_axis_id=research_axis_id)

                serializer = ResearchAxisSerializer(research_axis)
                data_research_axis = json.loads(json.dumps(serializer.data))

                research_axes_list.append(data_research_axis['subject'])

            x['research_axes'] = research_axes_list
        return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_times(request):
    all_times = Time.objects.all()
    serializer = TimeSerializer(all_times, many=True)

    data = json.loads(json.dumps(serializer.data))
    for time in data:
        if time['weekday'] == 'Saturday':
            time['weekday'] = 'شنبه'
        elif time['weekday'] == 'Sunday':
            time['weekday'] = 'یکشنبه'
        elif time['weekday'] == 'Monday':
            time['weekday'] = 'دوشنبه'
        elif time['weekday'] == 'Tuesday':
            time['weekday'] = 'سه‌شنبه'
        elif time['weekday'] == 'Wednesday':
            time['weekday'] = 'چهارشنبه'
        elif time['weekday'] == 'Thursday':
            time['weekday'] = 'پنج‌شنبه'
        elif time['weekday'] == 'Friday':
            time['weekday'] = 'جمعه'

        time['time'] = ':'.join(time['start_time'].split(':')[:2]) + "-" + \
                       ':'.join(time['end_time'].split(':')[:2])
        del time['start_time']
        del time['end_time']

    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_all_faculties(request):
    all_faculties = Faculty.objects.all()
    serializer = FacultySerializer(all_faculties, many=True)

    data = json.loads(json.dumps(serializer.data))
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def get_research_axes(request):
    faculty_id = request.query_params.get('faculty_id', None)
    search = request.query_params.get('search', None)

    if faculty_id is not None:
        try:
            Faculty.objects.get(id=faculty_id)
        except Faculty.DoesNotExist:
            return Response(f"Faculty with faculty_id {faculty_id} NOT FOUND!")
    else:
        return Response(f"Faculty_id: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

    if search is None:
        research_axes_to_show = ResearchAxis.objects.filter(faculty__id=faculty_id)
    else:
        research_axes_to_show = ResearchAxis.objects.filter(Q(faculty__id=faculty_id),
                                                            Q(faculty__name__icontains=search) |
                                                            Q(subject__icontains=search)
                                                            )

    serializer = ResearchAxisSerializer(research_axes_to_show, many=True)

    data = json.loads(json.dumps(serializer.data))
    for research_axis in data:
        del research_axis['faculty']

    return Response(data, status=status.HTTP_200_OK)


@permission_classes((IsAuthenticated,))
class UserGetProfessor(APIView):
    def get(self, args):
        professor_id = self.request.query_params.get('professor_id', None)
        if professor_id is not None:
            try:
                professor = Professor.objects.get(professor_id=professor_id)
            except Professor.DoesNotExist:
                return Response(f"Professor with professor_id {professor_id} NOT FOUND!",
                                status=status.HTTP_404_NOT_FOUND)

            serializer = ProfessorSerializer(professor)

            data = json.loads(json.dumps(serializer.data))

            del data['professor_id']
            del data['faculty']

            if data['academic_rank'] == 'Assistant Professor':
                data['academic_rank'] = 'استادیار'
            elif data['academic_rank'] == 'Associate Professor':
                data['academic_rank'] = 'دانشیار'
            elif data['academic_rank'] == 'Professor':
                data['academic_rank'] = 'استاد'

            free_times_list = []
            for free_time_id in data['free_times']:
                free_time = Time.objects.get(time_id=free_time_id)

                serializer = TimeSerializer(free_time)
                time_data = json.loads(json.dumps(serializer.data))

                if time_data['weekday'] == 'Saturday':
                    time_data['weekday'] = 'شنبه'
                elif time_data['weekday'] == 'Sunday':
                    time_data['weekday'] = 'یکشنبه'
                elif time_data['weekday'] == 'Monday':
                    time_data['weekday'] = 'دوشنبه'
                elif time_data['weekday'] == 'Tuesday':
                    time_data['weekday'] = 'سه‌شنبه'
                elif time_data['weekday'] == 'Wednesday':
                    time_data['weekday'] = 'چهارشنبه'
                elif time_data['weekday'] == 'Thursday':
                    time_data['weekday'] = 'پنج‌شنبه'
                elif time_data['weekday'] == 'Friday':
                    time_data['weekday'] = 'جمعه'

                time = time_data['weekday'] + ' ' + ':'.join(time_data['start_time'].split(':')[:2]) + "-" + \
                                                    ':'.join(time_data['end_time'].split(':')[:2])

                free_times_list.append(time)

            data['free_times'] = free_times_list

            research_axes_list = []
            for research_axis_id in data['research_axes']:
                research_axis = ResearchAxis.objects.get(research_axis_id=research_axis_id)

                serializer = ResearchAxisSerializer(research_axis)
                data_research_axis = json.loads(json.dumps(serializer.data))

                research_axes_list.append(data_research_axis['subject'])

            data['research_axes'] = research_axes_list
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response("Professor_id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)


@permission_classes((IsAuthenticated,))
class AdminProfessor(APIView):
    def post(self, args):
        user = self.request.user

        if user.role != 'admin-all':
            return Response("UNAUTHORIZED! You haven't been added as admin-all!", status=status.HTTP_401_UNAUTHORIZED)

        data = self.request.data

        if 'first_name' not in data:
            return Response("first_name: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

        if 'last_name' not in data:
            return Response("last_name: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

        if 'faculty_id' in data:
            try:
                faculty = Faculty.objects.get(id=data['faculty_id'])
            except Faculty.DoesNotExist:
                return Response(f"ERROR: Faculty with faculty_id {data['faculty_id']} NOT FOUND!",
                                status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("Faculty_id: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

        if 'email' not in data:
            return Response("email: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

        if 'academic_rank' not in data:
            return Response("academic_rank: None, BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)
        else:
            if data['academic_rank'] not in ['Professor', 'Assistant Professor', 'Associate Professor']:
                return Response('ERROR: academic_rank, BAD REQUEST!', status=status.HTTP_400_BAD_REQUEST)

        file = ""
        if 'filename' in data and 'image' in data:
            filename = data['filename']
            file = ContentFile(base64.b64decode(data['image']), name=filename)

        direct_telephone = ""
        if 'direct_telephone' in data:
            direct_telephone = data['direct_telephone']

        address = ""
        if 'address' in data:
            address = data['address']

        bachelor = ""
        if 'bachelor' in data:
            bachelor = data['bachelor']

        masters = ""
        if 'masters' in data:
            masters = data['masters']

        phd = ""
        if 'phd' in data:
            phd = data['phd']

        postdoctoral = ""
        if 'postdoctoral' in data:
            postdoctoral = data['postdoctoral']

        webpage_link = ""
        if 'webpage_link' in data:
            webpage_link = data['webpage_link']

        google_scholar_link = ""
        if 'google_scholar_link' in data:
            google_scholar_link = data['google_scholar_link']

        active = True
        if 'active' in data:
            if data['active'] == 'false':
                active = False
            elif data['active'] != 'true':
                return Response("Active: BAD REQUEST!", status=status.HTTP_400_BAD_REQUEST)

        if 'free_times_list' in data:
            for free_time_id in data['free_times_list']:
                try:
                    Time.objects.get(time_id=free_time_id)
                except Time.DoesNotExist:
                    return Response(f"Time with time_id {free_time_id} NOT FOUND!",
                                    status=status.HTTP_404_NOT_FOUND)

        if 'research_axes_list' in data:
            for research_axis_id in data['research_axes_list']:
                try:
                    ResearchAxis.objects.get(research_axis_id=research_axis_id)
                except ResearchAxis.DoesNotExist:
                    return Response(f"Research axis with research_axis_id {research_axis_id} NOT FOUND!",
                                    status=status.HTTP_404_NOT_FOUND)

        try:
            professor = Professor(first_name=data['first_name'],
                                  last_name=data['last_name'],
                                  faculty=faculty,
                                  image=file,
                                  academic_rank=data['academic_rank'],
                                  direct_telephone=direct_telephone,
                                  address=address,
                                  email=data['email'],
                                  bachelor=bachelor,
                                  masters=masters,
                                  phd=phd,
                                  postdoctoral=postdoctoral,
                                  webpage_link=webpage_link,
                                  google_scholar_link=google_scholar_link,
                                  active=active
                                  )

            professor.save()

            if 'free_times_list' in data:
                for free_time_id in data['free_times_list']:
                    time = Time.objects.get(time_id=free_time_id)
                    professor.free_times.add(time)

            if 'research_axes_list' in data:
                for research_axis_id in data['research_axes_list']:
                    research_axis = ResearchAxis.objects.get(research_axis_id=research_axis_id)
                    professor.research_axes.add(research_axis)

            professor.save()

            new_data = {'professor_id': professor.professor_id, 'message': "Professor has added successfully!"}
            return Response(new_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(f"ERROR: {e}", status=status.HTTP_400_BAD_REQUEST)

    def delete(self, args):
        user = self.request.user

        if user.role != 'admin-all':
            return Response("UNAUTHORIZED! You haven't been added as admin-all!", status=status.HTTP_401_UNAUTHORIZED)

        professor_id = self.request.query_params.get('professor_id', None)
        if professor_id is not None:
            try:
                professor = Professor.objects.get(professor_id=professor_id)
                professor.delete()
            except Professor.DoesNotExist:
                return Response(f"Redundant! Professor with professor_id {professor_id} NOT FOUND!",
                                status=status.HTTP_404_NOT_FOUND)

            return Response(f"Professor with professor_id {professor_id} removed successfully!",
                            status=status.HTTP_200_OK)
        else:
            return Response("Professor_id: None, BAD REQUEST", status=status.HTTP_400_BAD_REQUEST)
