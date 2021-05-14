import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/Users/Dom/chromedriver_win32/chromedriver.exe')
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')
    #неявное ожидание
    pytest.driver.implicitly_wait(5)
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('mariskab@rambler.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('ujhzxbqgbhju1985')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Нажимаем на кнопку "Мои питомцы"
    pytest.driver.find_element_by_css_selector("#navbarNav .nav-link[href='/my_pets']").click()

    yield

    pytest.driver.quit()

#проверяем, что присутствуют все питомцы
def test_my_pets():
    #явное ожидание
    element=WebDriverWait(pytest.driver, 5).until(EC.presence_of_element_located(('id','navbarNav')))
    #находим количество питомцев
    my_pets = len(pytest.driver.find_elements_by_xpath('//tbody/tr'))
    #количество питомцев в статистике
    my_pets_statistika = pytest.driver.find_element_by_xpath('//*[h2][1]').text.split()
    assert my_pets_statistika[3] == str(my_pets)


# проверяем, что хотя бы у половины питомцев есть фото
def test_my_pets_with_photo():
    #находим количество питомцев с фото
    my_pets_with_photo = pytest.driver.find_elements_by_css_selector('div#all_my_pets > table > tbody > tr > th > img')
    for i in range(len(my_pets_with_photo) // 2):
        assert my_pets_with_photo[i].get_attribute('src') != ''

#проверяем, что у всех есть имя, возраст, порода
def test_names_descr_ages():
    names = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
    poroda = pytest.driver.find_elements_by_xpath('//tbody/tr/td[2]')
    ages = pytest.driver.find_elements_by_xpath('//tbody/tr/td[3]')
    for i in range(len(names)):
        assert names[i].text != ''
        assert poroda[i].text != ''
        assert ages[i].text != ''

#проверяем, что не повторяющихся имен питомцев
def test_repeat_names():
    names = pytest.driver.find_elements_by_xpath('//tbody/tr/td[1]')
    #создаем пустой список для имен
    data_names = []
    #добавляем имена в список
    for name in names:
        name = name.text
        data_names.append(name)
    # Задаем счетчики i - для задания цикла перебора имен в списке и k - для подсчета повторяющихся имен питомцев
    i = 0
    k = 0
    # Проверяем список на наличие повторяющихся питомцев
    while i < len(data_names) - 1:
        if data_names[i] == data_names[i + 1]:
            k += 1

        i += 1

    assert k == 0







