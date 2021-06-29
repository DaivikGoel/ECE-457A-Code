import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;

public class Travel {
    private ArrayList<City> travel = new ArrayList();
    private ArrayList<City> previousTravel = new ArrayList();

    public Travel(int numberOfCities) {
        for (int i = 0; i < numberOfCities; i++) {
            travel.add(new City());
        }
    }

    //using the demand section as service time
    public Travel() {
        City[] cities = {
            new City("2", 79, 19, 18),
            new City("3", 41, 79, 16),
            new City("4", 25, 31, 22),
            new City("5", 63, 93, 24),
            new City("6", 33, 5, 3),
            new City("7", 69, 17, 19),
            new City("8", 57, 73, 6),
            new City("9", 53, 75, 6),
            new City("10", 1, 1, 6),
            new City("11", 79, 73, 12),
            new City("12", 59, 5, 18),
            new City("13", 1, 37, 16),
            new City("14", 41, 31, 72),
            new City("15", 23, 73, 7),
            new City("16", 37, 27, 16),
            new City("17", 85, 93, 23),
            new City("18", 93, 13, 4),
            new City("19", 85, 45, 22),
            new City("20", 49, 91, 23),
            new City("21", 55, 43, 7),
            new City("22", 83, 29, 11),
            new City("23", 93, 49, 11),
            new City("24", 87, 23, 1),
            new City("25", 31, 23, 22),
            new City("26", 19, 97, 16),
            new City("27", 41, 9, 15),
            new City("28", 83, 61, 7),
            new City("29", 9, 7, 5),
            new City("30", 13, 13, 22),
            new City("31", 43, 37, 9),
            new City("32", 13, 61, 10),
            new City("33", 71, 51, 11),
            new City("34", 45, 93, 9),
            new City("35", 93, 55, 3),
            new City("36", 5, 97, 7),
            new City("37", 81, 11, 15),
            new City("38", 7, 53, 10),
            new City("39", 7, 41, 2)
        };
        travel.addAll(Arrays.asList(cities));
    }

    public void generateCities() {
        if (travel.isEmpty())
            new Travel();
        Collections.shuffle(travel);
    }

    public void swapCities() {
        int a = generateRandomIndex();
        int b = generateRandomIndex();
        previousTravel = travel;
        City cityA = travel.get(a);
        City cityB = travel.get(b);
        travel.set(a, cityB);
        travel.set(b, cityA);
    }

    public void revertSwap() {
        travel = previousTravel;
    }

    private int generateRandomIndex() {
        return (int) (Math.random() * travel.size());
    }

    public City getCity(int index) {
        return travel.get(index);
    }

    public int getDistance(City endingDepot, City... startingCity) {
        int distance = 0;
        for (int index = 0; index < travel.size(); index++) {

            //startingCity is only used once at the very beginning to start from the depot
            City starting = startingCity == null ? getCity(index) : startingCity[0];
            startingCity = null;

            City destination;
            if (index + 1 < travel.size())
                destination = getCity(index + 1);
            else
                destination = endingDepot;

            distance += starting.distanceToCity(destination);
        }
        return distance;
    }

    public int getTime(int speed, City endingDepot, City... startingDepot) throws Exception {
        int totalTime = 0;

        for (int index = 0; index < travel.size(); index++) {
            City starting = startingDepot == null ? getCity(index) : startingDepot[0];
            startingDepot = null;

            City destination;
            if (index + 1 < travel.size())
                destination = getCity(index + 1);
             else
                destination = endingDepot;

            totalTime += starting.totalTimeToNextCity(destination, speed);
        }

        return totalTime;
    }
}
