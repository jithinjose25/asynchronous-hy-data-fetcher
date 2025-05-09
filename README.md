# asynchronous-hy-data-fetcher
Explore the asynchronous way of fetching hyd data from Water Survey of Canada

Asynchronous Hydrometric Data Fetcher is a tiny Python CLI tool that hits the WSC (Water Survey of Canada) GeoMet API, pulls daily‑mean discharge and water‑level records for any list of station numbers, and merges the results into a tidy Pandas DataFrame. Thanks to asyncio + httpx, it queries many stations in parallel, making large downloads dramatically faster than traditional one‑request‑at‑a‑time scripts.
