from data.basemodels import User
from data.collection import GetCasteWaifu, findWaifu
from data.database import checkWaifuDuplicate
from data.database import databaseSetup, getWaifu, storeWaifu
import os
import pytest


@pytest.fixture(autouse=True)
def resetDB():
    os.system('rm waifuUser.db')
    databaseSetup()


def createTestUser(totalValue: int):
    testUser = User(
        name="Saggins",
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


def test_GetCasteWaifu():
    assert GetCasteWaifu("SSS").favourites >= 12000
    assert GetCasteWaifu("SS").favourites >= 8000
    assert GetCasteWaifu("S").favourites >= 5400
    assert GetCasteWaifu("A").favourites >= 3700
    assert GetCasteWaifu("B").favourites >= 2000
    assert GetCasteWaifu("C").favourites >= 934
    assert GetCasteWaifu("D").favourites >= 525
