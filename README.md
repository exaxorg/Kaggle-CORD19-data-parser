This is a fast parser and CSV-file generator for the Kaggle challenge
"[COVID-19 Open Research Dataset Challenge
(CORD-19)](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge/)".
It transforms more than 68.000 JSON-files (8GB) into a single CSV file
in one minute on a modern laptop.

For more information, see this [blog post](https://exax.org/example/2020/04/13/covid.html).

*This is an [Accelerator](https://github.com/ebay/accelerator)
project, meaning that computations are fast, parallel, and
reproducible.* The Accelerator is an open source project from eBay.


Download Data and Create some Directories
-------------

1. Clone this repository.
   Then, `cd` into the created `Kaggle-CORD19-data-parser` directory.


1. Download the dataset `CORD-19-research-challenge.zip` from Kaggle
   [here](https://www.kaggle.com/allen-institute-for-ai/CORD-19-research-challenge).
   Unzip it.

   The default configuration assumes it is unzipped into a directory named `data/CORD-19-research-challenge`, so

   ```
   mkdir -p data/CORD-19-research-challenge
   unzip CORD-19-research-challenge.zip -d data/CORD-19-research-challenge
   ```


1. Create a "workdir", where all output will be stored, for example

   ```
   mkdir -p workdirs/cord
   ```


1. Create a "results" directory where results will be linked.

   ```
   mkdir results
   ```


Install and Run the Accelerator
-------------

1. Set up a virtual environment and install the Accelerator

   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install accelerator
   ```                                           


1. Read (and perhaps) modify the file `accelerator.conf`, in particular

   - set the number of `slices`, i.e. number of processes to run in parallel (for example `8`),
   - set the `workdirs` path to where output will be stored (for example `workdirs/cord`), and
   - set the `input directory` to the location of the unzipped CORD dataset (for example `data/CORD-19-research-challenge`).

   Make sure that the paths exists and are correct.
   

1. The Accelerator is a client-server application, so use two terminal
   emulator windows.  *Make sure to activate the virtual environment in
   both of them.*

   In the "server" terminal, type
   ```
   ax server
   ```

   In the "client" teminal, type
   ```
   ax run
   ```
   or
   ```
   ax run --fullpath
   ```

   The program will now execute.  It will print information about the build process and location of files.


The source code is found in the build script `dev/build.py`, which
calls the method `dev/a_import.py`.



License
-------

Copyright 2020 Anders Berkeman and Carl Drougge

Licensed under the Apache License, Version 2.0 (the "License"); you
may not use this file except in compliance with the License. You may
obtain a copy of the License at

```
https://www.apache.org/licenses/LICENSE-2.0
```

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
implied. See the License for the specific language governing
permissions and limitations under the License.
