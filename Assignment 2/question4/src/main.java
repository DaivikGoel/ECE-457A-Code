import java.util.*;

public class main {

    // both distance and time optimizations are done with one vehicle.
    public static void main(String[] args) {
        System.out.println("running question 4");

        int iterations = 10000, startingTemp = 15;
        double coolingRate = 0.9995;
        System.out.println(
            "Optimized distance of: " + SimulatedAnnealing.SADistance(25, 11000, 0.9994));

        try {
            System.out.println(
                    "Optimized Time of: " + SimulatedAnnealing.SATimeSpent(70, 40000, 0.9992, 70));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }




    //not used:
/*    private static List<int[]> assignCitiesToTrucks(int[][] cities, int[] depotCoord, int numTrucks) {
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
    }*/
}
