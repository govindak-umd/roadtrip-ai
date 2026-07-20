To run: 

    govindajithkumar@Mac roadtrip-ai % source .venv/bin/activate

Then: 


    (roadtrip-ai) govindajithkumar@Mac roadtrip-ai % uv run pytest -v     

You should then see a successful test run as follows:

    ================================================= test session starts =================================================
    platform darwin -- Python 3.13.9, pytest-9.1.1, pluggy-1.6.0 -- /Users/govindajithkumar/Desktop/roadtrip-ai/.venv/bin/python3
    cachedir: .pytest_cache
    rootdir: /Users/govindajithkumar/Desktop/roadtrip-ai
    configfile: pyproject.toml
    testpaths: backend/tests
    plugins: anyio-4.14.2
    collected 1 item                                                                                                      
    
    backend/tests/test_cost_engine.py::test_round_trip_cost PASSED                                                  [100%]
    
    ================================================= 1 passed in 12.20s ==================================================
    (roadtrip-ai) govindajithkumar@Mac roadtrip-ai % 


Now to access the swagger page:

    (roadtrip-ai) govindajithkumar@Mac roadtrip-ai % uv run uvicorn backend.app.main:app --reload

and go to:

http://127.0.0.1:8000/docs#/

    



