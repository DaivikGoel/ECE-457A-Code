import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;

public class Travel {

    private ArrayList<City> travel = new ArrayList<>();
    private ArrayList<City> previousTravel = new ArrayList<>();

    public Travel(int numberOfCities) {
        for (int i = 0; i < numberOfCities; i++) {
            travel.add(new City());
        }
    }

    public Travel() {
        City[] cities = {
            new City("1", 20, 20),
            new City("2",-20, 30),
            new City("3",25, 44),
            new City("4",42, 0),
            new City("5",10, -22),
            new City("6",15, -23),
            new City("6",1, -3)
        };
        travel.addAll(Arrays.asList(cities));
    }

    public void generateCities() {
        if (travel.isEmpty()) {
            new Travel();
            //new Travel(10);
        }
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

    public int getDistance(City... startingDepot) {
        int distance = 0;
        for (int index = 0; index < travel.size(); index++) {
            City starting = startingDepot == null ? getCity(index) : startingDepot[0];
            startingDepot = null;
//            City starting = getCity(index);
            City destination;
            if (index + 1 < travel.size()) {
                destination = getCity(index + 1);
            } else {
                destination = getCity(0);
            }
            distance += starting.distanceToCity(destination);
        }
        return distance;
    }
}
