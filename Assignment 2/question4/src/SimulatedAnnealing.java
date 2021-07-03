import java.text.DecimalFormat;

public class SimulatedAnnealing {

    private static Travel travel = new Travel();

    public static double SADistance(double startingTemperature, int numberOfIterations, double coolingRate) {
        DecimalFormat df = new DecimalFormat();
        df.setMaximumFractionDigits(3);

        System.out.println("Starting SA with temperature: " + startingTemperature + ", # of iterations: " + numberOfIterations + ", cooling rate: " + coolingRate);
        double temperature = startingTemperature;
        travel.generateCities();

        //this is the city(depot) we start and end at:
        City depot = new City("1",39, 19, 0);
        double bestDistance = travel.getDistance(depot, depot);
        System.out.println("Initial distance: " + bestDistance);

        Travel bestSolution = travel;
        Travel currentSolution = bestSolution;

        for (int i = 0; i < numberOfIterations; i++) {
            if (temperature > 0.1) {
                currentSolution.swapCities();
                double currentDistance = currentSolution.getDistance(depot, null);
                if (currentDistance < bestDistance) {
                    bestDistance = currentDistance;
                    System.out.println("----------found new best distance of: " + bestDistance + " at iteration #" + i);

                // e^(delta E - t) , delta E = bestDistance - currentDistance
                } else if (Math.exp((bestDistance - currentDistance) / temperature) < 1) {
                    currentSolution.revertSwap();
                }
                temperature *= coolingRate;

            } else
                continue;

            if (i % 100 == 0) {
                System.out.println("Iteration #" + i + ", current temp: " + String.format("%.03f", temperature) + " current best distance(KM): " + bestDistance);
            }
        }
        return bestDistance;
    }

    public static double SATimeSpent(double startingTemperature, int numberOfIterations, double coolingRate, int speed) throws Exception {

        System.out.println("Starting SA with temperature: " + startingTemperature + ", # of iterations: " + numberOfIterations + ", cooling rate: " + coolingRate);
        double temperature = startingTemperature;
        travel.generateCities();

        City depot = new City("1",39, 19, 0);
        double bestTime = travel.getTime(speed, depot, depot);
        System.out.println("Initial time: " + bestTime);

        Travel bestSolution = travel;
        Travel currentSolution = bestSolution;

        for (int i = 0; i < numberOfIterations; i++) {
            if (temperature > 0.1) {
                currentSolution.swapCities();
                double currentTime = currentSolution.getTime(speed, depot, null);
                if (currentTime < bestTime) {
                    bestTime = currentTime;
                    System.out.println("----------found new best time of: " + bestTime + " at iteration #" + i);

                // e^(delta E - t) , delta E = bestTime - currentTime
                } else if (Math.exp((bestTime - currentTime) / temperature) < 1) {
                    currentSolution.revertSwap();
                }
                temperature *= coolingRate;

            } else
                continue;

            if (i % 300 == 0) {
                System.out.println("Iteration #" + i + ", current temp: " + String.format("%.03f", temperature) + " current best time(in hours): " + bestTime);
            }
        }
        return bestTime;
    }
}
