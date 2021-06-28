import java.text.DecimalFormat;
import java.util.Optional;

public class SimulatedAnnealing {

    private static Travel travel = new Travel();

    public static double SA(double startingTemperature, int numberOfIterations, double coolingRate) {
        DecimalFormat df = new DecimalFormat();
        df.setMaximumFractionDigits(3);

        System.out.println("Starting SA with temperature: " + startingTemperature + ", # of iterations: " + numberOfIterations + ", cooling rate: " + coolingRate);
        double temperature = startingTemperature;
        travel.generateCities();

        City startingDepot = new City("1",39, 19, 0);
        double bestDistance = travel.getDistance(startingDepot);
        System.out.println("Initial distance: " + bestDistance);

        Travel bestSolution = travel;
        Travel currentSolution = bestSolution;

        for (int i = 0; i < numberOfIterations; i++) {
            if (temperature > 0.1) {
                currentSolution.swapCities();
                double currentDistance = currentSolution.getDistance(null);
                if (currentDistance < bestDistance) {
                    bestDistance = currentDistance;

                // e^(delta E - t) , delta E = bestDistance - currentDistance
                } else if (Math.exp((bestDistance - currentDistance) / temperature) < Math.random()) {
                    currentSolution.revertSwap();
                }
                temperature *= coolingRate;

            } else {
                continue;
            }

            if (i % 50 == 0) {
                System.out.println("Iteration #" + i + ", current temp: " + String.format("%.03f", temperature) + " current best distance of: " + bestDistance);
            }
        }
        return bestDistance;
    }
}
