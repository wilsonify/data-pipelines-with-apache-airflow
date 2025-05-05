"""
Create an admin user via Python script
"""
from airflow.models.auth import User
from airflow.utils.session import create_session
from airflow.security import permissions
from airflow.www.security_manager import AirflowSecurityManager


def create_admin_user():
    with create_session() as session:
        user = User()
        user.username = "admin"
        user.email = "admin@example.org"
        user._password = "admin"
        user.first_name = "Anonymous"
        user.last_name = "Admin"
        user.roles = [AirflowSecurityManager().find_role("Admin")]
        session.add(user)
        session.commit()


if __name__ == "__main__":
    create_admin_user()
