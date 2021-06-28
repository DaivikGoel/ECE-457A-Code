public class City {

    private int x;
    private int y;
    private int serviceTime;
    private String name;

    public City() {
        this.x = (int) (Math.random() * 500);
        this.y = (int) (Math.random() * 500);
    }

    public City(String city_name, int _x, int _y, int _serviceTime) {
        this.x = _x;
        this.y = _y;
        this.name = city_name;
        this.serviceTime = _serviceTime;
    }

    public void setX(int x) {
        this.x = x;
    }

    public void setY(int y) {
        this.y = y;
    }

    public int getX() {
        return x;
    }
    public int getY() {
        return y;
    }
    public int getServiceTime() { return serviceTime; }

    public double distanceToCity(City city) {
        int x = Math.abs(getX() - city.getX());
        int y = Math.abs(getY() - city.getY());
        return Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2));
    }
}
