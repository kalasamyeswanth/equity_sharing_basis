from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Investor, Investment

# My Investments view - lists the investments of the logged-in investor
@login_required
def my_investments(request):
    try:
        investor = Investor.objects.get(user=request.user)
        #investments = investor.investment_set.all()
    except Investor.DoesNotExist:
        return redirect('startup_list')
    investments = Investment.objects.filter(investor = investor)

    context = {
        'investments': investments,
    }
    return render(request, 'my_investments.html', context)

# Microshare Calculation view - shows calculated microshare for an investor
from decimal import Decimal
@login_required
def microshare_calculation(request, startup_id):
    #startup = Startup.object.get(id = startup_id)
    startup = get_object_or_404(Startup,id = startup_id)
    investment_amount = Decimal(startup.valuation)  # Example investment amount (USD)
    equity_taken = Decimal(startup.equity_offered)  # Example equity percentage

    # Calculate microshare value
    microshare_value = (investment_amount * equity_taken) / 100
    
    context = {
        'investment_amount': investment_amount,
        'equity_taken': equity_taken,
        'microshare_value': microshare_value,
    }
    return render(request, 'microshare_calculation.html', context)

# Solar Panel Cost Calculation view - shows the total cost of solar panels
@login_required
def solar_panel_cost_calculation(request, startup_id):

    panel_cost = 300  # Cost per solar panel (USD)
    num_panels = 20  # Number of panels

    # Calculate total cost
    total_cost = panel_cost * num_panels

    context = {
        'panel_cost': panel_cost,
        'num_panels': num_panels,
        'total_cost': total_cost,
    }
    return render(request, 'solar_panel_cost_calculation.html', context)


def inverstment(request):
    return render(request,'investment.html')














from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import Startup, Investor, Investment
from .forms import InvestmentForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.
class StartupListView(LoginRequiredMixin,ListView):
    model = Startup
    template_name = 'startup_list.html'
    context_object_name = 'startups'
    paginate_by = 10  # You can paginate if there are many startups


class StartupDetailView(DetailView):
    model = Startup
    template_name = 'startup_detail.html'
    context_object_name = 'startup'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['investment_form'] = InvestmentForm()
        return context


def startupdetail(request, pk):
    startup = get_object_or_404(Startup,id = pk)
    investment_amount = Decimal(startup.valuation)  
    equity_taken = Decimal(startup.equity_offered)
    investments = Investment.objects.filter(startup = startup)
    
    microshare_value = (investment_amount * equity_taken) / 100
    
    context = {
        'investments': investments,
        'name': startup.name,
        'description': startup.description,
        'founder': startup.founder,
        'investment_amount': investment_amount,
        'equity_taken': equity_taken,
        'microshare_value': microshare_value,
    }
    return render(request, 'startup_detail.html', context)











@login_required
def invest_create(request):
    if request.method == 'POST':
        form = InvestmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('myapp1:startup_list')
    else:
        form = InvestmentForm()
    return render(request, 'invest_in_startup.html', {'form': form})

































@login_required
def invest_in_startup(request, pk):
    startup = get_object_or_404(Startup, pk=pk)

    if not hasattr(request.user, 'investor'):
        messages.error(request, "Only investors can make investments.")
        return redirect('startup_detail', pk=startup.pk)

    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.startup = startup
            investment.investor = request.user.investor

            total_equity_invested = sum(i.equity_taken for i in Investment.objects.filter(startup=startup))
            if total_equity_invested + investment.equity_taken > startup.equity_offered:
                messages.error(request, "Not enough equity remaining for this investment.")
                return redirect('startup_detail', pk=startup.pk)

            investment.save()
            messages.success(request, "Investment successful!")
            return redirect('startup_detail', pk=startup.pk)
    else:
        form = InvestmentForm()

    return render(request, 'invest_in_startup.html', {'form': form, 'startup': startup})


