CREATE EXTENSION pg_cron;

GRANT USAGE ON SCHEMA cron TO cameo;

-- Scheduled task to remove deprecated otps
SELECT cron.schedule('0 0 * * *', $$DELETE 
    FROM otps
    WHERE expiration_time < now() - interval '1 days'$$);