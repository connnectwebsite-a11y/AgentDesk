
import sqlite3
from datetime import datetime

DB_NAME = "agentdesk.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def get_ticket_by_id(ticket_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT ticket_id, created_at, problem,
               response, status, notes
        FROM tickets
        WHERE ticket_id = ?
    """, (ticket_id.strip().upper(),))

    ticket = cursor.fetchone()
    connection.close()

    return ticket


def get_all_tickets():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT ticket_id, created_at, problem, status
        FROM tickets
        ORDER BY id DESC
    """)

    tickets = cursor.fetchall()
    connection.close()

    return tickets


def update_ticket_status(ticket_id, new_status):

    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved"
    ]

    if new_status not in allowed_statuses:
        return False

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
    """, (
        new_status,
        ticket_id.strip().upper()
    ))

    connection.commit()
    updated = cursor.rowcount
    connection.close()

    return updated > 0


def add_ticket_note_history(ticket_id, note):

    if not note or not note.strip():
        return False

    created_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO ticket_notes
        (ticket_id, note, created_at)
        VALUES (?, ?, ?)
    """, (
        ticket_id.strip().upper(),
        note.strip(),
        created_at
    ))

    connection.commit()
    connection.close()

    return True


def get_ticket_notes(ticket_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT note, created_at
        FROM ticket_notes
        WHERE ticket_id = ?
        ORDER BY id DESC
    """, (ticket_id.strip().upper(),))

    notes = cursor.fetchall()
    connection.close()

    return notes
