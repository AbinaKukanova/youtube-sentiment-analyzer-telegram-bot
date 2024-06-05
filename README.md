# project-212-AbinaKukanova
project-212-AbinaKukanova created by GitHub Classroom


Ccылка на проект http://AbinaKukanova.pythonanywhere.com/


Выполнила Куканова Абина, группа 212 

Я создала телеграм бот, которому на вход подается ссылка на видео в Youtube, он парсит комментарии под видео и в конце выводит график соотношения негативных и положительных ответов. Для того, чтобы бот начал работу, нужно ввести команду /search_videos. После этого он выведет вам предложение, что бот начал работать и нужно будет подождать, пока он выведет нам график. 

Для создания проекта я использовала модель логистичесской регрессии, чтобы предсказать негативные и положительные комментарии. Для тестовых данных я использовала датасет c русско-язычными комментариями под отрицательными постами в твиттере, которые были уже разделены на негативные и положительные. Для парсинга комментариев воспользовалась python библиотекой Selenium которая с помощью модуля WebDriver позволяет автоматизировать действия в браузере предоставляя для их реализации API. В файле model_regr лежит модель и функции для очистки текста и стоп-слов. И в файле config.py лежит информация о хосте и токене.  


