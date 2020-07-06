# path-search
The experimental python3 implementations of shortest path search (A* algorithm, Dijkstra algorith).

## requirements

||version|
|:--|:--|
|python|3.8.1|
|pillow|7.1.2|

## Example of elapsed time
* Environment
  * iMac (Retina 5K, 27-inch, 2017), 4.2 GHz Intel Core i7, 32 GB 2400 MHz DDR4
  * macOS Mojave, 10.14.6
  * Nodes: 50 x 50

|algorithm|example of elapsed time(sec)|
|:--|:--|
|A*|4.088|
|Dijkstra|5.747|
|A* (improved by refrring [Implementing Fast Heuristic Search Code](https://www.aaai.org/ocs/index.php/SOCS/SOCS12/paper/viewFile/5404/5682))|0.037|

![sample graph & path](../images/fast_astar_path.jpg)

## License

[MIT License](/LICENSE)