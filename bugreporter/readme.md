-------
Система bug-reportов, по типу issueв с GH
-------
DarkTracker может и имеет:
- Система пользователей (Сессии)
- Создавать большие проекты
- В проектах есть стадии которые можно создавать
- Репорты (У каждого репорта должна быть стадия)
- У репортов есть комментарии и тэги
- Система защиты через токены url/backend/gettoken
Самые важные ссылки:
login/ - login
logout/ - logout
registration/ - registration
projects/NICKNAME/ - all project of this user
projects/NICKNAME/delete/ID/ - delete project
projects/NICKNAME/PROJECT/ - all report of this projects
projects/NICKNAME/PROJECT/REPORTID/comments/ - all comments of this bug
backend/gettoken - get POST token
projects/NICKNAME/PROJECT/stages/ - all stages
projects/NICKNAME/PROJECT/stages/delete/ID - delete stage
projects/NICKNAME/PROJECT/REPORTID/stage/ - PIN stage
projects/NICKNAME/PROJECT/tags/ - all projects tag
projects/NICKNAME/PROJECT/REPORTID/addtag/ - PIN tag
projects/NICKNAME/PROJECT/REPORTID/deltag/ID - UNPIN tag
projects/NICKNAME/PROJECT/REPORTID/alltags/ - All tags