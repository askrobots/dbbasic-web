#!/usr/bin/env python3
"""Management CLI for dbbasic-web"""
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py [command]")
        print("\nCommands:")
        print("  serve     - Run the development server")
        print("  worker    - Run the background job worker")
        print("  shell     - Start interactive shell")
        sys.exit(1)

    command = sys.argv[1]

    if command == "serve":
        serve()
    elif command == "worker":
        worker()
    elif command == "shell":
        shell()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


def serve():
    """Run the development server"""
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))

    print(f"Starting dbbasic-web on http://{host}:{port}")
    uvicorn.run(
        "dbbasic_web.asgi:app",
        host=host,
        port=port,
        reload=True,
        log_level="info",
    )


def worker():
    """Run background job worker"""
    from dbbasic_web.jobs import process_jobs
    import time

    print("Starting job worker...")
    while True:
        try:
            process_jobs()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nWorker stopped")
            break
        except Exception as e:
            print(f"Worker error: {e}")
            time.sleep(5)


def shell():
    """Start interactive shell with app context"""
    import code
    from dbbasic_web import settings
    from dbbasic_web.storage import write_text, read_text
    from dbbasic_web.jobs import enqueue
    from dbbasic_web.bus import EventBus

    context = {
        "settings": settings,
        "write_text": write_text,
        "read_text": read_text,
        "enqueue": enqueue,
        "EventBus": EventBus,
    }

    banner = "dbbasic-web interactive shell\nAvailable: settings, write_text, read_text, enqueue, EventBus"
    code.interact(banner=banner, local=context)


if __name__ == "__main__":
    main()
