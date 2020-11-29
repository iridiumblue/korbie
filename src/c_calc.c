// 3D array is static, hand-assemble returning value
// for windows, get GCC like this - https://dev.to/gamegods3/how-to-install-gcc-in-windows-10-the-easier-way-422j


#include <math.h>
#include <stdlib.h>
#include <stdio.h>

#undef NDEBUG  // trigger asserts in release builds as well as debug builds
#include <assert.h>   // reinclude the header to update the definition of assert()

#define PI M_PI


#define MAX_STEPS 200000*3
#define NUM_SCALARS 3

static int NUM_STEPS=20000;

static double x_s[MAX_STEPS][NUM_SCALARS];

double Delta(double a, double r) 
{
  return r*r -2*r + a*a;
}

double f_d(double a, double r, double zm)
{
  return (r*r + a*a*zm*zm) * Delta(a, r);
}

double f_h(double a, double r, double zm)
{
    return r*(r-2) + zm*zm/(1-zm*zm)*Delta(a, r);
}

double f_g(double a, double r)
{
    return 2*a*r;
}

double f_f(double a, double r, double zm)
{
    return (r*r*r*r) + a*a*(r*(r+2) + zm*zm*Delta(a,r));
}

void calc_ELQ(double a, double p, double e, double theta_min, double result[])
{
    
    double rmax = p/(1.-e);
    double rmin = p/(1.+e);
    
    double zm = cos(theta_min);
    
    double kappa, epsilon, rho, eta, sigma;
    if (e != 0) {
        kappa     = f_d(a, rmin, zm)*f_h(a, rmax, zm) - f_h(a, rmin, zm)*f_d(a, rmax, zm);

        epsilon = f_d(a, rmin, zm)*f_g(a, rmax)     - f_g(a, rmin)*f_d(a, rmax, zm);
        rho     = f_f(a, rmin, zm)*f_h(a, rmax, zm) - f_h(a, rmin, zm)*f_f(a, rmax, zm);
        eta        = f_f(a, rmin, zm)*f_g(a, rmax)     - f_g(a, rmin)*f_f(a, rmax, zm);
        sigma    = f_g(a, rmin)*f_h(a, rmax, zm)     - f_h(a, rmin, zm)*f_g(a, rmax);
    }
    double aa=kappa*rho + 2.0*epsilon*sigma - 2.0*sqrt(sigma*(sigma*epsilon*epsilon + rho*epsilon*kappa - eta*kappa*kappa));
    double bb = rho*rho + 4*eta*sigma;

    double E = sqrt(aa/bb);
 
    double L = (2*f_g(a, rmin)*E - sqrt(4*f_g(a, rmin)*f_g(a, rmin)*E*E + 4*f_h(a, rmin, zm)*(f_f(a, rmin, zm)*E*E - f_d(a, rmin, zm))))/(-2*f_h(a, rmin, zm));
    double Q=0.0;
    if (theta_min == PI/2.0) {
        Q = 0;
    } else {
        Q = zm*zm*(a*a*(1-E*E) + L*L/(1-zm*zm));
    }

    result[0]=E; result[1]=L; result[2]=Q;
    //return [E,L,Q]
}

double Psi(double psi,double M,double E,double p3,double p4,double p,double e) 
{
    return (M*sqrt((1. - E*E)*((p-p3) - e*(p + p3*cos(psi)))*((p-p4) + e*(p-p4*cos(psi)))) )/(1. - e*e);
}

double X(double chi,double E,double zp,double zm,double a) 
{
    return sqrt(a*a*(1.0-E*E)*(zp - zm*cos(chi)*cos(chi)));
}

double r_psi(double p, double e, double psi) 
{
    return p/(1 + e*cos(psi));
}

double cosTheta(double chi,double ang_inc)
{
    return cos(ang_inc)*cos(chi);
}

double Phi(double psi,double chi,double E,double L,double e,double p,double a,double ang_inc)
{
    double r = r_psi(p,e,psi);
    return a/Delta(a,r)*(E*(r*r + a*a) - a*L) + L/(1. - cosTheta(chi,ang_inc)*cosTheta(chi,ang_inc)) - a*E;
}

void ode_system(double *x, double t,double E,double L,double M,double p3,double p4,double zp,double zm,double p,
    double e,double a,double ang_inc, double h,double *y)
{
       //y = [0,0,0]
       //x=_x.flatten()
    
       y[0] = Psi(x[0],M,E,p3,p4,p,e)*h;
       y[1] = X(x[1],E,zp,zm,a)*h;
       y[2] = Phi(x[0],x[1],E,L,e,p,a,ang_inc)*h;
       //return np.array(y,dtype=np.double32)
}

void sum3(double *a, double k,double * b, double *c) 
{
   for (int i=0; i<3; i++) {
       c[i] = a[i]+k*b[i];
   }
}

void print3(double *a)
{
    printf("[%f,%f,%f]\n",a[0],a[1],a[2]);
}

void test_rk4(double a,double  p,double  e, double ang_inc, double *t, int sz_t, double x[MAX_STEPS][NUM_SCALARS] )
{
    /*
        """Fourth-order Runge-Kutta method to solve x' = f(x,t) with x(t[0]) = x0.

        USAGE:
            x = rk4(f, x0, t)

        INPUT:
            f     - function of x and t equal to dx/dt.  x may be multivalued,
                    in which case it should a list or a NumPy array.  In this
                    case f must return a NumPy array with the same dimension
                    as x.
            x0    - the initial condition(s).  Specifies the value of x when
                    t = t[0].  Can be either a scalar or a list or NumPy array
                    if a system of equations is being solved.
            t     - list or NumPy array of t values to compute solution at.
                    t[0] is the the initial condition point, and the difference
                    h=t[i+1]-t[i] determines the step size h.

        OUTPUT:
            x     - NumPy array containing solution values corresponding to each
                    entry in t array.  If a system is being solved, x will be
                    an array of arrays.
        """
        */
        //a=0.95
        //#p=3.1
        //#e=0.0001
        ang_inc = ang_inc/180.0*PI + PI/2;
        
        double ELQ[3];
        calc_ELQ(a,p,e,ang_inc,ELQ);
        double E=ELQ[0]; double L=ELQ[1]; double Q=ELQ[2];
        double M=1;
        double r1 = p/(1.-e);
        double r2 = p/(1.+e);

        double AplusB = 2.*M/(1.0 - E*E) - (r1 + r2);
        double AB = a*a*Q/((1.0 - E*E)*r1*r2);

        double r3 = (AplusB + sqrt(AplusB*AplusB - 4.*AB))/2.0;
        double r4 = AB/r3;

        double eps0 = a*a*(1. - E*E)/(L*L);
        double zm = cos(ang_inc)*cos(ang_inc);
        double zp = Q/(L*L*eps0*zm);

        double p3 = r3*(1.-e)/M;
        double p4 = r4*(1.+e)/M;
        double x0[3];
        //double x[2000][3] = {0.0};
        int n=NUM_STEPS;
        x[0][0]=0.3; x[0][1]=0.2; x[0][2]=0.1;
        double h,k1[3],k2[3],k3[3],k4[3];
        double nx[3];
        for (int i=0; i<n-2; i++) {
            //printf("--- %d \n",i);
            h = t[i+1] - t[i];
            ode_system( x[i], t[i],E,L,M,p3,p4,zp,zm,p,e,a, ang_inc,h,k1);
            //print3(k1);
            sum3(x[i],0.5,k1,nx);
            //print3(nx);
            ode_system( nx, t[i] + 0.5 * h ,E,L,M,p3,p4,zp,zm,p,e,a, ang_inc, h, k2 );
            sum3(x[i],0.5,k2,nx);
            //print3(x[i+1]);
            ode_system( nx, t[i] + 0.5 * h ,E,L,M,p3,p4,zp,zm,p,e,a, ang_inc, h, k3 );
            sum3(x[i],1,k3,nx);
            //print3(x[i+1]);
            ode_system( nx, t[i+1] ,E,L,M,p3,p4,zp,zm,p,e,a, ang_inc, h, k4 );
            sum3(k2,1.0,k3,nx);
            
            sum3(k1,2.0,nx,nx);
            
            sum3(k4,1.0,nx,nx);
            //print3(nx);
            for (int j=0; j<3; j++) {nx[j]=nx[j]/6.0;}
            sum3(x[i],1.0,nx,x[i+1]);
            // rotate into place
            // WARNING - remove these temp variables for performance.
            double psi=x[i+1][0]; 
            double chi=x[i+1][1]; 
            double phi=x[i+1][2];
            double r = r_psi(p, e, psi);
            double rx = r*cos(phi)*sin(acos(cosTheta(chi,ang_inc)));
            
            double ry = r*sin(phi)*sin(acos(cosTheta(chi,ang_inc)));
            double rz = r*cos(acos(cosTheta(chi,ang_inc)));
            //re-use existing data struct for results
            x[i][0]=rx; x[i][1]=ry; x[i][2]=rz;



            
            //x[i+1] = x[i] + ( k1 + 2.0 * ( k2 + k3 ) + k4 ) / 6.0;
            //return;
        }
        //clobber last (null) point
        x[n-2][0]=x[n-3][0]; x[n-2][1]=x[n-3][1]; x[n-2][2]=x[n-3][2]; 
        x[n-1][0]=x[n-2][0]; x[n-1][1]=x[n-2][1]; x[n-1][2]=x[n-2][2]; 
        
}

int go(float a, float p, float e, float ang_inc, double t[], double x[MAX_STEPS][NUM_SCALARS])
{
    //int NUM_STEPS=5000;
    //double x[NUM_STEPS][3] = {0.0};
    /*
    double t[NUM_STEPS];
    for (int i=0; i<NUM_STEPS; i++) {
        t[i]=i*M_PI/500.0;
        //x[i][0]=i*0.01;
    }
    */
    
    //double aa=0.5;
    //double p=8;
    //double e=0.3;
    //double ang_inc=45;

    test_rk4(a, p, e, ang_inc, t, NUM_STEPS, x );
    
    /*
    for (int i=0; i<100; i++) {
        printf("-- %d --\n",i);
        print3(x[i]);

    }
    */
    //printf("%f %f %f", x[1000][0],x[1000][1],x[1000][2]);
    //exit(0);

    return 0;
}

extern "C" {
  void go_4(
        float a, float p, float e, float theta,
        double t[],double x[], uint num_steps
       )
  {
      if (num_steps>MAX_STEPS) {
          fprintf(stderr,"num_steps > %d .  Bailing.", MAX_STEPS);
          exit(0);
      }
      NUM_STEPS=num_steps;
      //assert(NUM_STEPS==num_steps);
      printf("Got through!!!\n");
      printf("C engine : %d steps.\n", num_steps);
      go(a,p,e,theta,t,x_s);
      for (int i=0; i<NUM_STEPS;i++) {
          for (int j=0; j<NUM_SCALARS; j++) {
              int ij=i*NUM_SCALARS+j;
              x[ij]=x_s[i][j];
          }
      }
      //int y=1;
      //printf("%lf ", x[2000][1]);

  }
}
/*
int main( void ) {

    go();


}
*/
