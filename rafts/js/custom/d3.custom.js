import * as d3 from "https://cdn.jsdelivr.net/npm/d3@7/+esm";
import * as crossfilter from "https://cdn.jsdelivr.net/npm/crossfilter2@1/crossfilter";
import * as dc from "https://cdn.jsdelivr.net/npm/dc@4/dc";
data = d3.csv("../../_data/intoxicate/intoxicate.patient_registry.stable.csv");
ndx = crossfilter(data);
