import java.util.*;

public class main {

    public static void main(String[] args) {
        System.out.println("running question 4");
/*
        location[] cities = {
                new location(2, 2, "1"),
                new location(-2, 3, "2"),
                new location(2, 4, "3"),
                new location(4, 0, "4"),
                new location(0, -2, "5")
        };
        int[][] cities = {{2,2}, {-2,3}, {2,4}, {4,0}, {0, -2}};
        int[] depotCoord = {0, 0};
        List<int[]> ordering = assignCitiesToTrucks(cities, depotCoord, 2);
        ordering.forEach(array -> System.out.println(Arrays.toString(array)));
*/

        int iterations = 10000, startingTemp = 10;
        double coolingRate = 0.9995;
        System.out.println(
            "Optimized distance of: " + SimulatedAnnealing.SA(25, 10000, 0.9995));
    }

    private static List<int[]> assignCitiesToTrucks(int[][] cities, int[] depotCoord, int numTrucks) {
        int depotX = depotCoord[0], depotY = depotCoord[1];

        List<int[]> list = new ArrayList<>();
        //sort based on euclidean distance to the depot, minimize travel time
        PriorityQueue<int[]> pq = new PriorityQueue<int[]>((a, b) ->
                ((b[0]-depotX) * (b[0]-depotX) + (b[1]-depotY) * (b[1]-depotY)) -
                    ((a[0]-depotX) * (a[0]-depotX) + (a[1]-depotY) * (a[1]-depotY)));

        for (int[] c : cities)
            pq.offer(c);

        while (!pq.isEmpty()) {
            int[] city = pq.remove();
            list.add(city);
        }

        return list;
    }
}
