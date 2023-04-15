import pytest
from rest_framework.test import APIClient
from model_bakery import baker
import random

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)

    return factory


@pytest.fixture
def students_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_create_course_factory(client, course_factory):
    courses = course_factory(_quantity=1)

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == courses[0].name


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_courses_by_name(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    data = response.json()
    for i, c in enumerate(data):
        assert c['name'] == courses[i].name


@pytest.mark.django_db
def test_courses_by_id(client, course_factory):
    courses = course_factory(_quantity=10)

    response = client.get('/api/v1/courses/')

    assert response.status_code == 200
    random_id = courses[random.randint(0, len(courses) - 1)].id
    response = client.get(f'/api/v1/courses/{random_id}/')
    data = response.json()
    assert random_id == data['id']


@pytest.mark.django_db
def test_create_course(client):
    course_name = 'test_name'
    response = client.post('/api/v1/courses/', data={'name': course_name})

    assert response.status_code == 201
    data = response.json()
    assert data['name'] == course_name


@pytest.mark.django_db
def test_update_course_factory(client, course_factory):
    courses = course_factory(_quantity=1)

    course_name = 'update_name'
    response = client.patch(f'/api/v1/courses/{courses[0].id}/', data={'name': course_name})

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == course_name


@pytest.mark.django_db
def test_delete_course_factory(client, course_factory):
    courses = course_factory(_quantity=1)

    response = client.delete(f'/api/v1/courses/{courses[0].id}/')

    assert response.status_code == 204
