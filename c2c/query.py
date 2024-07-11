import duckdb
import time

print('start')
start = time.time()
duckdb.sql('install spatial;load spatial;')
duckdb.sql("""
    WITH areas AS (
        SELECT names.primary as name,
               ST_GeomFromWKB(geometry) as area_geom
        FROM '../data/bretagne-division_area.parquet'
        WHERE subtype = 'county' and region = 'FR-BRE'
        ),
    schools AS (
        SELECT ST_GeomFromWKB(geometry) as school_geom
        FROM '../data/bretagne-place.parquet'
        WHERE categories.main = 'school'
        )
    SELECT name, area_geom, count(school_geom) as school_count
    FROM areas JOIN schools ON ST_Contains(area_geom, school_geom)
    GROUP BY area_geom, name
""").show()

print("--- %s ms ---" % ((time.time() - start) * 1000))
