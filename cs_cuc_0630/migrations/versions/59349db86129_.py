"""empty message

Revision ID: 59349db86129
Revises: None
Create Date: 2016-04-16 12:36:04.378279

"""

# revision identifiers, used by Alembic.
revision = '59349db86129'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('StudentAct',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_sort', sa.String(length=255), nullable=True),
    sa.Column('student_lable', sa.String(length=255), nullable=True),
    sa.Column('student_theme', sa.String(length=255), nullable=True),
    sa.Column('student_content', sa.Text(), nullable=True),
    sa.Column('student_imgsrc', sa.String(length=255), nullable=True),
    sa.Column('student_endcontent', sa.Text(), nullable=True),
    sa.Column('student_update', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('classes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('classes_sort', sa.String(length=255), nullable=True),
    sa.Column('classes_lable', sa.String(length=255), nullable=True),
    sa.Column('classes_theme', sa.String(length=255), nullable=True),
    sa.Column('classes_content', sa.Text(), nullable=True),
    sa.Column('classes_imgsrc', sa.String(length=255), nullable=True),
    sa.Column('classes_endcontent', sa.Text(), nullable=True),
    sa.Column('classes_update', sa.String(length=255), nullable=True),
    sa.Column('classes_brief', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('collegeNews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('news_sort', sa.String(length=255), nullable=True),
    sa.Column('news_lable', sa.String(length=255), nullable=True),
    sa.Column('news_theme', sa.String(length=255), nullable=True),
    sa.Column('news_content', sa.Text(), nullable=True),
    sa.Column('news_imgsrc', sa.String(length=255), nullable=True),
    sa.Column('news_endcontent', sa.Text(), nullable=True),
    sa.Column('news_update', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('teachers_sort', sa.String(length=255), nullable=True),
    sa.Column('teachers_lable', sa.String(length=255), nullable=True),
    sa.Column('orderid', sa.Integer(), nullable=True),
    sa.Column('teachers_content', sa.Text(), nullable=True),
    sa.Column('teachers_imgsrc', sa.String(length=255), nullable=True),
    sa.Column('teachers_endcontent', sa.Text(), nullable=True),
    sa.Column('teachers_update', sa.String(length=255), nullable=True),
    sa.Column('teachers_brief', sa.Text(), nullable=True),
    sa.Column('teachers_icon', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('teachers')
    op.drop_table('collegeNews')
    op.drop_table('classes')
    op.drop_table('StudentAct')
    ### end Alembic commands ###
