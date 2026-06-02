# TCCT Transport Mode Detection

## Credit
```
@article{carpineti18,
  Author = {Claudia Carpineti, Vincenzo Lomonaco, Luca Bedogni, Marco Di Felice, Luciano Bononi},
  Journal = {Proc. of the 14th Workshop on Context and Activity Modeling and Recognition (IEEE COMOREA 2018)},
  Title = {Custom Dual Transportation Mode Detection by Smartphone Devices Exploiting Sensor Diversity},
  Year = {2018}
  DOI = {https://doi.org/10.1109/PERCOMW.2018.8480119}
}
```
The preprocessing codes are re-written and modified codes from [US-TransportationMode](https://github.com/vlomonaco/US-TransportationMode).

## How to run
Download the [raw data](https://cs.unibo.it/projects/us-tm2017/static/dataset/raw_data/raw_data.tar.gz) and place in under `data/`

Run the following commands in order
```
docker compose --profile preprocess up --build
docker compose --profile train up --build
```

The output models will be located under `models/[config-hash]/`

## Notes
Running the following command:
```
docker compose --profile preprocess up --build
```

is equivalent to running the following commands sequentially:

```
docker compose --profile extract up --build
docker compose --profile clean up --build
docker compose --profile transform up --build
```