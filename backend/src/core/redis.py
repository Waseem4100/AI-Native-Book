"""
Redis and Python-RQ queue initialization.

This module configures Upstash Redis connection and Python-RQ job queue
for async content generation tasks.
"""

from typing import Optional

import redis
from rq import Queue

from .config import settings

# Global Redis connection
_redis_client: Optional[redis.Redis] = None
_generation_queue: Optional[Queue] = None


def get_redis_client() -> redis.Redis:
    """
    Get Redis client connection.

    Creates a new connection if one doesn't exist.

    Returns:
        redis.Redis: Redis client instance

    Raises:
        redis.ConnectionError: If connection fails
    """
    global _redis_client

    if _redis_client is None:
        _redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_keepalive=True,
        )
        # Test connection
        _redis_client.ping()

    return _redis_client


def get_generation_queue() -> Queue:
    """
    Get Python-RQ queue for content generation jobs.

    Creates a new queue if one doesn't exist.
    Uses the default job timeout from settings (5 minutes per spec).

    Returns:
        Queue: RQ queue for generation jobs

    Usage:
        queue = get_generation_queue()
        job = queue.enqueue(generate_chapter_content, chapter_id=123)
    """
    global _generation_queue

    if _generation_queue is None:
        redis_client = get_redis_client()
        _generation_queue = Queue(
            name="textbook_generation",
            connection=redis_client,
            default_timeout=settings.JOB_TIMEOUT,  # 300 seconds per spec
        )

    return _generation_queue


def clear_queue() -> int:
    """
    Clear all jobs from the generation queue.

    Useful for testing and maintenance.

    Returns:
        int: Number of jobs cleared
    """
    queue = get_generation_queue()
    count = len(queue)
    queue.empty()
    return count


def get_job_status(job_id: str) -> dict:
    """
    Get the status of a job by ID.

    Args:
        job_id: RQ job ID

    Returns:
        dict: Job status information including:
            - status: pending, started, finished, failed
            - result: Job result if finished
            - error: Error message if failed
            - progress: Progress information if available
    """
    queue = get_generation_queue()
    job = queue.fetch_job(job_id)

    if not job:
        return {"status": "not_found", "error": "Job not found"}

    status = {
        "id": job.id,
        "status": job.get_status(),
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "started_at": job.started_at.isoformat() if job.started_at else None,
        "ended_at": job.ended_at.isoformat() if job.ended_at else None,
    }

    if job.is_finished:
        status["result"] = job.result
    elif job.is_failed:
        status["error"] = str(job.exc_info)

    # Add progress if available (set via job.meta)
    if job.meta:
        status["progress"] = job.meta.get("progress")

    return status


def initialize_redis() -> None:
    """
    Initialize Redis connection on application startup.

    Tests the connection and creates the generation queue.

    Raises:
        redis.ConnectionError: If connection fails
    """
    try:
        client = get_redis_client()
        client.ping()
        get_generation_queue()
        print("✅ Redis and Python-RQ queue initialized")
    except redis.ConnectionError as e:
        print(f"❌ Redis connection failed: {e}")
        raise


def cleanup_redis() -> None:
    """
    Cleanup Redis connection on application shutdown.

    Closes the connection gracefully.
    """
    global _redis_client

    if _redis_client is not None:
        _redis_client.close()
        _redis_client = None
        print("✅ Redis connection closed")
