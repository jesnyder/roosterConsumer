# mapClinical
An interactive map of clinical trials using a mesenchymal stromal cell (MSC) therapeutic intervention. Group the trials based on the source of the MSCs - allogeneic, autologous, both, or undeclared. All trials are assigned to one group.

Explore the map here:
https://jesnyder.github.io/mapClinical/

Watch an introduction to the map here:
https://youtu.be/wNrNCIRuCok

The tasks to build the map include:

1. Build database: All clinical trial data comes from the NIH database maintained by the US National Library of Medicine - ClinicalTrials.gov (https://clinicaltrials.gov). We accessed the data using a combination of manual and automated searches conducted through the application programming interface (API) (https://clinicaltrials.gov/api/) and a python wrapper (https://pytrials.readthedocs.io/en/latest/readme.html). Our focus was clinical trials that use a mesenchymal stromal cell therapy. The nomenclature of MSC has changed over the years - from mesenchymal stem cell to mesenchymal stromal cell. The term "mesenchymal" could be conflated with results for "mesenchyme" - the general term for connective tissue. To find trials with MSC therapies, we listed search terms that would lead to MSC cells - "mesenchymal stromal" and "mesenchymal stem", referenced MSC source tissue - "mesenchymal umbilical cord" or "mesenchymal placental", and tradenames for MSC therapies - "mesenchymal Alofisel" and "mesenchymal "CardioCell". A complete list of search terms is included in this repo under user_provided>admin>search_terms.csv. There is a 1000 trial max download using the automated scraper, so if the results for an automated search term were the maximum allowable, we conducted a manual search, download, and save to capture the full record. This was only required for "mesenchymal stem". Once scraped or downloaded, all trials were coregistered using their URL on ClinicalTrials.gov (which includes their ID number) as a unique identifier to prevent duplicate entries.

2. Assign groups: Search the description, title, intervention, and outcome fields of each trial in the database for terms indicative of either an allogeneic or autologous source. If one or more allogeneic terms are found, then the trial is assigned to the allogeneic group. Terms included "allogeneic", as well as trade names for allogeneic MSC products, and sources of MSCs that must be allogeneic, like placenta and umbilical cord. A full list of allogeneic terms can be found and edited in user_provided>admin>allo_terms.csv. Autologous trials were grouped using the same approach, except using terms saved in the file user_provided>admin>auto_terms.csv. If terms from both the allogeneic and autologous lists are found, then the trial is assigned to the "both" group. If no terms from either group are found, then the trial is assigned to the "undeclared" group. Each trial is assigned to only one group.

3. Geolocate trials: Search the "Locations" field of each trial to find all the locations of the trials. Some trials have multiple locations that are separated by the '|' character. Save a list of all the unique locations to program_generated>locations>locations.csv Lookup the latitude and longitude for each location using the OpenStreetMap API (https://www.openstreetmap.org).

4. Write geojson: Coregister the ClinicalTrials.gov trial data with the geolocated locations. Prepare geojson for each group according to standards set by the Internet Engineering Task Force (https://geojson.org/). For each group, a javascript file is written containing a unique variable with the group name that is set equal to the geojson and saved as a ".js" file in the docs>js location.   

4. Annual counts: Count the number of trials and participants enrolled for all the trials and for each group.

5. Summarize fields: List unique fields for all the trials
