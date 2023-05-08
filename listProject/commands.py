import click
from listProject import db, app
from listProject.models import User


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop db.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('DB Ready.')


@app.cli.command()
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True)
# hide_input 隐藏输入
# confirmation_prompt 二次确认
def admin(username, password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating ...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating ...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')

