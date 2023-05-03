Below is a task: Port Scanner.

It is required to develop a web application for scanning open TCP ports on a remote host.

The application must implement the following REST API:

GET /scan//<begin_port>/<end_port>

Parameters:

    # ip - host to be scanned
    
    # begin_port - start of port range to scan
    
    # end_port - end of port range to scan

Handler for this url - starts scanning the specified host, and gives information to the client. In JSON format (can be in parts).

Response format: [{"port": "integer", "state": "(open|close)"}]

Program requirements: Aiohttp (>= 3.2.0), Python3.5 or higher;

the presence of application operation logs - incoming requests, errors, etc. Logging must be done in syslog.

It will be a plus: the presence of tests (AioHTTPTestCase), not necessary but desirable;

a ready-made spec file for building an RPM package with the program.

Preferred implementation: Fedora 31 system image.

Result: code hosted on a git repository (eg github).

In Russian:
Ниже тестовое задание: 
Сканер портов
Требуется разработать web-приложение для сканирования открытых TCP поротв удаленного хоста.
Приложение должно реализовать следующее REST API:
* GET /scan/<ip>/<begin_port>/<end_port>

Параметры:
    # ip - хост, который необходимо просканировать
    # begin_port - начала диапозона портов для сканирования
    # end_port - конец диапозона портов для сканирования

Обработчик данного урла - запускает сканирование указанного хоста, и отдает информацию клиенту. В формате JSON (можно частями).
Формат ответа: [{"port": "integer", "state": "(open|close)"}]
Требования к программе:
Aiohttp (>= 3.2.0), Python3.5 или выше;
наличие логов работы приложения - входящие запросы, ошибки и т.д. Логирование необходимо производить в syslog.
Будет плюсом:
наличие тестов (AioHTTPTestCase), не обязательно но желательно;
готовый spec-файл для сборки RPM-пакета с программой.
Предпочтительные средства реализации:
образ системы Fedora 31.
Результат:
код, расположенный на git-репозитории (например, github).
