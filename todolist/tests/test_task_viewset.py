import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Task
from user.models import CustomUser


@pytest.fixture
def api_client():
    client = APIClient()
    user = CustomUser.objects.create_user(
        email='testuser@gmail.com', password='password')
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def create_task():
    def _create_task(title="Sample Task", completed=False):
        return Task.objects.create(title=title, completed=completed)
    return _create_task


@pytest.mark.django_db
def test_create_task(api_client):
    url = reverse('task-list')
    print(url)
    data = {'title': 'New Task', 'completed': False}
    response = api_client.post(url, data, format='json')
    print(response)
    assert response.status_code == status.HTTP_201_CREATED
    assert Task.objects.filter(title='New Task').exists()


@pytest.mark.django_db
def test_list_tasks(api_client, create_task):
    create_task(title='Task 1')
    create_task(title='Task 2')
    url = reverse('task-list')
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data['results']) == 2  # Assuming pagination is enabled


@pytest.mark.django_db
def test_retrieve_task(api_client, create_task):
    task = create_task(title='Retrieve Task')
    url = reverse('task-detail', args=[task.id])
    response = api_client.get(url, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Retrieve Task'


@pytest.mark.django_db
def test_update_task(api_client, create_task):
    task = create_task(title='Old Title')
    url = reverse('task-detail', args=[task.id])
    data = {'title': 'Updated Title', 'completed': True}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    task.refresh_from_db()
    assert task.title == 'Updated Title'
    assert task.completed is True


@pytest.mark.django_db
def test_delete_task(api_client, create_task):
    task = create_task(title='Delete Task')
    url = reverse('task-detail', args=[task.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Task.objects.filter(id=task.id).exists()


@pytest.mark.django_db
def test_filter_tasks(api_client, create_task):
    create_task(title='Completed Task', completed=True)
    create_task(title='Incomplete Task', completed=False)
    url = reverse('task-list')
    response = api_client.get(url, {'completed': True}, format='json')
    assert response.status_code == status.HTTP_200_OK
    for task in response.data['results']:
        assert task['completed'] is True


@pytest.mark.django_db
def test_search_tasks(api_client, create_task):
    create_task(title='Searchable Task')
    create_task(title='Another Task')
    url = reverse('task-list')
    response = api_client.get(url, {'search': 'Searchable'}, format='json')
    assert response.status_code == status.HTTP_200_OK
    for task in response.data['results']:
        assert 'Searchable' in task['title']
