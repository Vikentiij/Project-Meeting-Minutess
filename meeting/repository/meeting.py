from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas


def get_all(db: Session):
    meetings = db.query(models.Meeting).all()
    return meetings


def create(meeting: schemas.Meeting, user_id: int, db: Session):
    new_meeting = models.Meeting(title=meeting.title, date=meeting.date, attendants=meeting.attendants, user_id=user_id)
    db.add(new_meeting)
    db.commit()
    db.refresh(new_meeting)
    return new_meeting


def destroy(id: int, db: Session):
    meeting = db.query(models.Meeting).filter(models.Meeting.id == id)
    if not meeting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with id {id} not found")

    topics = meeting.first().topics
    for topic in topics:
        topic_to_delete = db.query(models.Topic).filter(models.Topic.id == topic.id)
        topic_to_delete.delete(synchronize_session=False)
        db.commit()

    meeting.delete(synchronize_session=False)
    db.commit()

    return "meeting deleted"


def update(id:int, request: schemas.Meeting, db:Session):
    meeting=db.query(models.Meeting).filter(models.Meeting.id == id)
    if not meeting.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Meeting with id {id} not found")

    meeting.update(values={
        "title": request.title,
        "date": request.date,
        "attendants": request.attendants,
    })
    db.commit()
    return "updated"


def show(id: int, db: Session):
    meeting = db.query(models.Meeting).filter(models.Meeting.id == id).first()
    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Meeting with id {id} is not avaliable",
        )

    # response.status_code = status.HTTP_404_NOT_FOUND
    # return{"detail":f"Meeting with id {id} is not avaliable"}
    return meeting


def create_topic(meeting_id, new_topic, db):
    new_topic = models.Topic(meeting_id=meeting_id, topic=new_topic.topic, raised_by=new_topic.raised_by, actions_required=new_topic.actions_required, action_by=new_topic.action_by, to_be_action_by=new_topic.to_be_action_by)
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic


def update_topic(meeting_id, updated_topic, db):
    topic_to_update = db.query(models.Topic).filter(models.Topic.meeting_id == meeting_id).filter(models.Topic.id == updated_topic.id)
    if not topic_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic {updated_topic.id} for meeting {meeting_id} not found",
        )

    topic_to_update.update(values={
        "topic": updated_topic.topic,
        "raised_by": updated_topic.raised_by,
        "actions_required": updated_topic.actions_required,
        "action_by": updated_topic.action_by,
        "to_be_action_by": updated_topic.to_be_action_by,
    })
    db.commit()
    return "updated"


def get_topic(meeting_id, topic_id, db):
    topic = db.query(models.Topic).filter(models.Topic.meeting_id == meeting_id).filter(models.Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic {topic_id} for meeting {meeting_id} not found",
        )
    return topic


def delete_topic(meeting_id, topic_id, db):
    topic_to_delete = db.query(models.Topic).filter(models.Topic.meeting_id == meeting_id).filter(models.Topic.id == topic_id)
    if not topic_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Topic {topic_id} for meeting {meeting_id} not found",
        )

    topic_to_delete.delete(synchronize_session=False)
    db.commit()

    return "Topic deleted"
