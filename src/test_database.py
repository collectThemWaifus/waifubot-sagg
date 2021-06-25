from basemodels import User, Waifu
from collection import findWaifu
from database import checkWaifuDuplicate, databaseSetup, getWaifu, storeWaifu
import os
import pytest

@pytest.fixture(autouse=True)
def resetDB():
    try:
        os.system('rm waifuUser.db')
    except:
        pass
    databaseSetup()


def createTestUser(totalValue : int):
    testUser = User(
        name="Saggins",
        avatarURL="https://cdn.discordapp.com/avatars/185918091685920768/4b6ce0c047564ae3d9508089dd611b97.png",
        totalValue=totalValue,
        userId=185918091685920768
        )
    return testUser

def test_checkWaifuDuplicate():
    testWaifuList = findWaifu(2, 1)
    testWaifu = testWaifuList[0]
    storeWaifu(testWaifu, 185918091685920768)
    assert checkWaifuDuplicate(testWaifu.name)
    
    newTestWaifu = testWaifuList[1]
    assert not checkWaifuDuplicate(newTestWaifu.name)

def test_StoreGetWaifu():
    testWaifu = findWaifu(1, 1)[0]
    storeWaifu(testWaifu, 185918091685920768)
    assert testWaifu == getWaifu(185918091685920768)[0]
    assert not getWaifu(12345677889)
