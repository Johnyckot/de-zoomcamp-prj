-- Docs: https://docs.mage.ai/guides/sql-blocks
-- select f from test2323;
-- select year,month,day, count(*) from de_zoomcamp_dataset.test_repo_ex
-- group by year,month,day

-- select '{{ variables("test_var") }}' 
-- MERGE INTO de_zoomcamp_dataset.dim_repo tgt
-- USING
-- (
--   select id as repo_id , name as repo_name, url as repo_url from de_zoomcamp_dataset.stage_repo_external
--   where 
--   year = 2024
--   and month = 3
--   and day = 20
-- ) src
-- ON tgt.repo_id = src.repo_id 
-- WHEN MATCHED 
--   AND( tgt.repo_name != src.repo_name 
--    OR tgt.repo_url != src.repo_url)
-- THEN UPDATE
--   SET 
--   tgt.repo_name = src.repo_name,
--   tgt.repo_url = src.repo_url
-- WHEN NOT MATCHED THEN 
--  INSERT (repo_id, repo_name, repo_url)
--  VALUES (src.repo_id, src.repo_name, src.repo_url)


-- DROP TABLE IF EXISTS de_zoomcamp_dataset.dim_repo ;
-- CREATE TABLE IF NOT EXISTS de_zoomcamp_dataset.dim_repo (
--   repo_id NUMERIC(20,0) OPTIONS (description = 'Repository ID'),
--   repo_name  STRING OPTIONS (description = 'Repository name'),
--   repo_url  STRING OPTIONS (description = 'Repository URL')  
-- ) 
-- CLUSTER BY
--   repo_id
-- OPTIONS (    
--     description = 'Repository dimension'
-- )
-- ;


