# Incident 001 - Payment Service Crash

Date: 2026-08-01

Service: payment-service

Environment: Kubernetes

Problem:
The payment-service pod repeatedly entered CrashLoopBackOff.

Observed Error:
Connection refused while connecting to PostgreSQL.

Investigation:
The application configuration contained an incorrect
database service hostname.

Expected:
postgres-service

Configured:
postgres-db-service

Root Cause:
Incorrect database service name in the application
configuration.

Resolution:
Changed DB_HOST to postgres-service and redeployed
the application.

Lesson:
When a pod enters CrashLoopBackOff, application logs
should be checked before changing Kubernetes resources.
