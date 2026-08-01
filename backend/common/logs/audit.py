"""
Audit logging helpers. Every admin action, order change, and user
change should be recorded via log_action() for the AuditLogs table.
"""


def log_action(actor_id, action: str, target_type: str, target_id, metadata: dict | None = None):
    """Persist an audit log entry.

    NOTE: wire this to the apps.analytics AuditLog model once migrations exist.
    """
    # TODO: create AuditLog row
    pass
