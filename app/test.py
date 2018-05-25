import os
import click
from app import app

@app.cli.comand()
@click.argument('name')
def create_user(name):
    """Create user"""
    pass
