import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from db.queries.users import delete_user, update_user_data


class TestUserApiAuth:
    
    @pytest.mark.anyio
    async def test_get_user(self, async_client_auth):
        response = await async_client_auth.get('/user/get_user')

        assert response.status_code == 200
#     
    @pytest.mark.anyio
    async def test_user_update_data(self, async_client_auth, test_update_data_user,
            test_register_user, db_session: AsyncSession):
        response = await async_client_auth.patch('/user/update_user', json=test_update_data_user)

        assert response.status_code == 200

        await update_user_data(db_session, test_update_data_user['login'],
                login=test_register_user['login'])


    @pytest.mark.anyio
    async def test_logout(self, async_client_auth):
        response = await async_client_auth.get('/user/logout')
        assert response.status_code == 200

class TestUserNonAuth:

    @pytest.mark.anyio
    async def test_get_user(self, async_client):
        response = await async_client.get('/user/get_user')
        assert response.status_code == 403


    @pytest.mark.anyio
    async def test_logout(self, async_client):
        response = await async_client.get('/user/logout')
        assert response.status_code == 403

    @pytest.mark.anyio
    async def test_register(self, async_client, test_user):
        response = await async_client.post('/user/create_user', json=test_user)
        assert response.status_code == 201
        

    @pytest.mark.anyio
    async def test_regiser_existinig_user(self, async_client, test_user):
        response = await async_client.post('/user/create_user', json=test_user)
        assert response.status_code == 400

    @pytest.mark.anyio
    async def test_login(self, async_client, test_user, db_session: AsyncSession):
        response = await async_client.post('/user/login', json={
                'login': test_user['login'],
                'password': test_user['password']
            })
        assert response.status_code == 200
        await delete_user(db_session, test_user['login'])

