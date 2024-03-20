FROM archlinux:latest

WORKDIR /terminusbot

ENV FLASK_APP=app.py

RUN pacman -Syu --noconfirm && pacman -S --noconfirm python python-pip supervisor nginx
COPY supervisord.conf /etc/supervisor/conf.d/

COPY requirements.txt requirements.txt
RUN pip install --break-system-packages -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
